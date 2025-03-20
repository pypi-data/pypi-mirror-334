from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from PIL import Image

from turftopic.base import ContextualModel

UrlStr = str

ImageRepr = [Image | UrlStr]


@dataclass
class EmbeddingStore:
    document_embeddings: np.ndarray
    image_embeddings: list[tuple[np.ndarray]]

    @property
    def joint_embeddings(self) -> np.ndarray:
        embeddings = []
        for e_document, e_images in zip(
            self.document_embeddings, self.image_embeddings
        ):
            stacked_embeddings = np.atleast_2d(
                np.stack([e_document, *e_images])
            )
            embeddings.append(np.mean(stacked_embeddings, axis=0))
        return np.stack(embeddings)


def _load_images(images: Iterable[ImageRepr]) -> Iterable[Image]:
    for image in images:
        if isinstance(image, str):
            image = Image.open(image)
        yield image


def _encode_images(encoder, images: Iterable[tuple[ImageRepr] | ImageRepr]):
    image_embeddings = []
    for im in images:
        if not isinstance(im, tuple):
            im = (im,)
        im = list(_load_images(im))
        image_embeddings.append(tuple(encoder.encode(im)))


class MultimodalModel(ContextualModel):

    def encode_joint(
        self,
        raw_documents: Iterable[str],
        images: Iterable[tuple[ImageRepr] | ImageRepr],
    ) -> EmbeddingStore:
        document_embeddings = self.encoder_.encode(raw_documents)
        image_embeddings = _encode_images(self.encoder_, images)
        if document_embeddings.shape[0] != len(image_embeddings):
            raise ValueError("Images and documents were not the same length.")
        return EmbeddingStore(
            document_embeddings=document_embeddings,
            image_embeddings=image_embeddings,
        )

    @abstractmethod
    def fit_transform_multimodal(
        self,
        raw_documents: Iterable[str],
        images: Iterable[tuple[ImageRepr] | ImageRepr],
        y=None,
    ) -> np.ndarray:
        pass

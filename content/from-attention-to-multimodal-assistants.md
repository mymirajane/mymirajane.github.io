---
title: "From attention to multimodal assistants"
date: 2026-10-25
draft: false
slug: from-attention-to-multimodal-assistants
type: writing
description: "A short map of how VQA architectures moved from image grids toward richer image-language interaction."
---
The history of visual question answering can be read as a series of attempts to connect the right words to the right parts of an image. My report compared several influential designs, and the progression is easier to understand when viewed through that one question.

## Where should the model look?

Stacked Attention Networks (SAN) used the question to inspect a grid of image features in successive steps. Bottom-up and top-down attention moved toward detected object regions, then used the question to weight those regions. That made the visual units more object-centered, while also making the system dependent on its detector.

## How should image and text interact?

Simple fusion can concatenate or multiply one image vector and one question vector. Bilinear Attention Networks (BAN) instead model interactions between image regions and individual question words. Modular Co-Attention Networks (MCAN) stack self-attention and cross-modal attention so each side can refine what it takes from the other.

## What changed with generative models?

Systems such as LLaVA connect visual features to a language model, which can generate a natural-language answer rather than choose from a fixed answer vocabulary. That creates new possibilities for explanation and open-ended response, alongside new questions about grounding and reliability.

No single architecture erases the central challenge. The model still has to connect the question to the image and answer from evidence rather than from a convenient guess. This post is adapted from the architecture survey in my March 2026 VQA report.

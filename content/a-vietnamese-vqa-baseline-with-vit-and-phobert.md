---
title: "A Vietnamese VQA baseline with ViT and PhoBERT"
date: 2026-10-25
draft: false
slug: a-vietnamese-vqa-baseline-with-vit-and-phobert
type: writing
tags: "VQA, Vietnamese, experiment"
description: "How I combined frozen image and language encoders, and what the training results revealed."
---
For the implementation section of my VQA report, I built a baseline that combines a Vision Transformer for images with [PhoBERT](https://huggingface.co/vinai/phobert-base) for Vietnamese questions. The point of this experiment was to see how much a relatively small trainable fusion and classification head could learn from pretrained features.

## The setup

Images were resized to 224 × 224 pixels and normalized for the vision model. Questions were tokenized to at most 64 tokens. I froze both pretrained encoders and trained the fusion and classifier layers, which reduced the number of parameters I had to update.

- Vision encoder: vit_base_patch16_224.
- Question encoder: vinai/phobert-base.
- Training: 10 epochs, batch size 32, learning rate 0.001.
- Tracked metrics: standard accuracy, VQA-style accuracy, and Average Normalized Levenshtein Similarity (ANLS).

## What the numbers said

Training loss fell from 3.8304 in epoch 1 to 0.8607 in epoch 10. Training accuracy rose from 22.72% to 75.16%. The strongest validation accuracy in the report was 46.40% at epoch 6; the same checkpoint recorded a validation top-5 VQA score of 74.00% and ANLS of 0.4462.

After epoch 6, validation accuracy stayed around 42–46% even as the training score kept improving. That gap is a reminder that fitting the training set and generalizing to new image-question pairs are different things. In this run, stopping around epoch 6 or 7 would have saved time without losing the best reported validation result.

## Possible next checks

The aggregate scores do not show which questions failed. Useful next checks would include errors by question type, frequent versus rare answers, and whether the model relies too heavily on wording instead of image evidence. Those checks could say more about its strengths and limitations than one accuracy figure.

These are results from my course project, as recorded in the March 2026 report. They are not a claim of state-of-the-art benchmark performance.

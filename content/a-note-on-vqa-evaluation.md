---
title: "A note on VQA evaluation"
date: 2026-10-25
draft: false
slug: a-note-on-vqa-evaluation
type: note
tags: "VQA, evaluation"
description: "One image question can have more than one reasonable answer."
---
Exact-match accuracy can hide useful nuance in visual question answering. If annotators give different but compatible answers, a prediction may deserve partial credit rather than a binary wrong label. My VQA project tracked both conventional accuracy and measures designed to recognize agreement or small text differences.

The metric should reflect the kind of mistake we care about. A spelling variation is different from an answer that ignores the image entirely.

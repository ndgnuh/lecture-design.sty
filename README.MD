# lecture-design.sty

A LaTeX package for designing teaching materials.

## Install

Clone the repository and run:
```bash
make install
```

If you use LyX, also run reconfigure in LyX's GUI.

## Usage

### Preamble

```tex
\usepackage{lecture-design}
```

### Theorems and proofs

```tex
\begin{theorem}
    This is a theorem.
    \begin{proof}
    This is a proof.
    \end{proof}
\end{theorem}
```

By default, proofs WON'T be shown. The proofs must be shown manually using this command:
```tex
\ShowProofs
```

### Problems and solutions

```tex
\begin{problem}
    This is a problem.
    \begin{solution}
    This is a solution.
    \end{solution}
\end{problem}   
```

Similarly, solutions WON'T be shown by default. Use this command to show them:
```tex
\ShowSolutions
```

### Markings/tags

I use tags to mark the problems' roles in the lecture. The predefined marks are:
```tex
\ExampleMark{} % This question should be used as an example.
\QuickMark{} % This question is for quick practice.
\AnswerMark{Answer} % This question has an answer provided.
\OfficialIndexMark{Index} % This question is from the official index.
\MustDoMark{} % This question is recommended to be done.
\DangerMark{} % This question is dangerous/difficult.
```

Custom mark labels can be defined using:
```tex
\SetMarkLabel{<MarkName>}{<LabelText>}
```

New marks can be defined using:
```tex
\NewMark{<MarkName>}{<BackgroundColor>}{<Border/TextColor>}
% or marks with extra text
\NewMark*{<MarkName>}{<BackgroundColor>}{<Border/TextColor>}
```

### Localization

To localize the package to another language, redefine the following commands in the preamble:

```tex
\def\problemname{Bài tập}
\def\definitionname{Định nghĩa}
\def\theoremname{Định lý}
\def\proofname{Chứng minh}
\def\solutionname{Lời giải}
\def\remarkname{Chú ý}
\def\TypesetProofSection#1{Chứng minh cho #1}
\def\TypesetSolutionSection#1{Lời giải cho~#1}
\SetMarkLabel{SolutionHint}{Giải:~tr.\,}
\SetMarkLabel{ProofHint}{C/M:~tr.\,}
\SetMarkLabel{Example}{Ví dụ}
\SetMarkLabel{Quick}{Chữa nhanh}
\SetMarkLabel{Answer}{Ans:~}
\SetMarkLabel{Official index}{Index:~}
\SetMarkLabel{Must-do}{Nên chữa}
\SetMarkLabel{Danger}{[!]~}
```

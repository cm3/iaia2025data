# Metadata for the Correspondence between Public Comments and the Final Plan Revisions

## Title
Correspondence between Public Comments and Revisions in the Sixth Basic Environment Plan (Draft to Final Proposal)

## Creator
- Akihiro Kameda (亀田 尭宙)  
    - ORCID: [0000-0002-5439-6456](https://orcid.org/0000-0002-5439-6456)  
    - Affiliation: National Institutes for the Humanities  
    - Position: Project Assistant Professor  
- Kohei Ishii（石井 康平）  
    - Affiliation: Chiba University  
    - Position: Ph.D. Student  

## Description
This dataset documents the relationship between public comments and subsequent revisions made between two versions of the Sixth Basic Environment Plan. It provides structured analysis on whether and how revisions reflected public input.

### Columns in `diff_and_corresp.csv` (final output):
- **Column A**: Assigned ID of each revision  
- **Column B**: Page number where the revision occurs  
- **Columns B–E**: Content of the revision, including insertion, deletion, and contextual text  
- **Column F**: Category of revision  
- **Column G**: Rationale for classification  
- **Column H**: Flag indicating whether the revision was based on a public comment (1 = Yes)  

## Language
Japanese

## Version
1.0

## Date Issued
2025-05-02

## License
- Dataset files (CSV/HTML): [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- Python scripts: [METS License](https://www.loc.gov/standards/mets/METS-LICENSE.txt)

## Repository URL
[https://github.com/cm3/iaia2025data](https://github.com/cm3/iaia2025data)

## Related Document
An abstract with detailed explanation will be published on the [IAIA2025 Website](https://2025.iaia.org/pages/abstract.php)

---

## Processes and Related Files

### 1. Preprocessing (`preprocessing/`)

#### Overview  
- The final plan with visible revisions (資料2-2) was downloaded from the Ministry of the Environment Japan:  
  [https://www.env.go.jp/council/02policy/41124_00010.html](https://www.env.go.jp/council/02policy/41124_00010.html)  
- This PDF was converted via Microsoft Word to HTML (`input.html`).
- Revisions were extracted using `extract.py` and merged with context using `merge_diff.py`.

#### Files
- `input.html`: HTML version of the final plan with visible changes  
- `extract.py`: Script to extract differences from HTML  
- `diff_output.csv`: Extracted modifications  
- `merge_diff.py`: Script to merge and group adjacent differences  
- `merged_diff_output.csv`: Merged list of structured revision entries  

---

### 2. Classification (`classification/`)

#### Overview  
- The file `merged_diff_output.csv` was classified using ChatGPT-based prompting via `chatgpt_classify.py`.  
- The classification output is saved in `merged_with_classification.csv` and then integrated into the final `diff_and_corresp.csv`.

#### Classification Categories (based on a Japanese-language prompt)

1. **Particles and Format Normalization（てにをは、フォーマットの正規化）**  
   Minor adjustments to particles and formatting (e.g., kanji → hiragana, half-width → full-width).  
   *Example*: “更に” → “さらに”, “2.1℃” → “２．１℃”, “は” → “が”

2. **Numerical Updates（数字のアップデート）**  
   Updates to figures such as years or statistics.  
   *Example*: “2023” → “2024”, “30%” → “35%”, “50万人” → “52万人”

3. **Abbreviation Expansion and Citation Completion（略語・正式名称への変換、引用・出典の補完）**  
   Expanded abbreviations or added legal references.  
   *Example*: “COP28” → “第28回締約国会議（COP28）”, inserting “（平成xx年法律第yy号）”

4. **Rhetorical Adjustments and Structural Rewriting（修辞の調整、語順変更や文構造整理）**  
   Clarifying or strengthening statements, changing word order.  
   *Example*: “～が望まれる” → “～が必要である”

5. **Other Minor Meaning-Preserving Edits（その他意味に踏み込まない変更）**  
   Punctuation, spacing, and other non-substantive changes.

6. **Other Meaning-Altering Edits（その他意味に踏み込んだ変更）**  
   Substantive modifications affecting the content or meaning.

#### Files
- `chatgpt_classify.py`: Script to classify revisions via ChatGPT prompts  
- `merged_with_classification.csv`: Classified revision list with rationale  
- `diff_and_corresp.csv`: Final dataset (includes classification and comment correspondence flag)  

---

### 3. Comment–Revision Matching (`matching/`)

#### Overview  
- The file `6thPC_AnalysisData_full_20250209.csv` contains evaluations of public comments and government responses, developed for presentation at the 2025 Annual Conference of the Japanese Society for Artificial Intelligence.
- The script `get_corresp.py` infers one-to-many correspondences between comments and revision entries.  
- Specific instructions were given to focus on matching based on actual responsiveness, not mere topical relevance.

#### Files
- `6thPC_AnalysisData_full_20250209.csv`: Evaluated public comments and responses  
- `get_corresp.py`: Script for comment-revision matching  
- `pabukome_matched_changes.csv`: Estimated comment-to-revision mapping  
- `merged_diff_output.csv`: Reused structured list of revision entries  

---

## Integration

The final output file `diff_and_corresp.csv` was created by combining the results of classification and matching.  
The H column reflects inferred links between comments and revisions.


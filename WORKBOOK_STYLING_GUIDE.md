WORKBOOK STYLING GUIDE

1. DESIGN INTENT

The workbook should feel like a serious, management-ready investment model.
Disciplined, low-noise, traceable, and structurally familiar to leadership.
Use color sparingly and consistently. Keep the workbook mostly white with dark text.

2. FONT AND TEXT

Font:
- Arial 8 across the entire workbook with no exceptions
- do not vary font face or size anywhere, including titles, notes, and outputs

Emphasis:
- use bold, fill color, font color, borders, and spacing to create hierarchy
- never use font size for hierarchy

Percentage rule:
- every cell containing a percentage value must be italicized
- this applies on top of whatever font color the cell already uses
- blue input percentage = blue italic; black formula percentage = black italic; green linked percentage = green italic
- no exceptions

3. ROW HEIGHT, GRIDLINES, PANES, AND TEXT WRAP

Row height:
- one universal row height of 10.0 across the entire workbook
- no taller title rows, no shorter detail rows
- do not go below 10.0

Gridlines:
- hidden on every tab

Frozen panes:
- none anywhere in the workbook

Text wrap:
- never enabled on any cell in any tab
- if text does not fit, shorten the label, abbreviate, split across adjacent cells, or move detail to a note column or the source log
- no exceptions

4. COLUMN WIDTHS

- primary row-label column: 24 to 34
- secondary label or helper columns: 10 to 18
- annual time-series columns: 10 to 12
- monthly or milestone timing columns: 8 to 10
- spacer columns: 2 to 3

5. CELL-TYPE COLOR LEGEND

Text color:
- blue = hardcoded numeric input (quantities, rates, percentages, dollar amounts, years used as assumptions)
- black = formula on the same tab, or hand-entered text labels, category names, descriptions, and string data
- green = link from another tab in the workbook
- red = external link or externally sourced value needing careful sourcing
- gray = static label, memo, locked historical, helper text, source references, and notes columns

Blue-text decision rule:
- blue applies to numeric values that a human typed rather than a formula or cross-tab link producing
- text strings remain black even when hand-entered; the blue signal is reserved for numbers that drive calculations, not static labels or categorical data
- a locked numeric assumption is still a hardcode; a management-set target rate is still a hardcode
- applying blue to every hand-typed string (agency names, class names, descriptions) creates visual noise and defeats the purpose of the convention
- the only black numbers are formula outputs on the same tab
- the only green values are references pulled from other tabs
- when in doubt about a number: did a formula produce this value on this tab? If no, it is blue
- when in doubt about text: leave it black unless it is a source reference or note, in which case it is gray
- range values stored as text (e.g., "5-35", "0-3", "<1") are not numeric hardcodes and should remain black

Background fill:
- white = normal model body
- very light yellow (RGB 255, 249, 196) = editable assumption cell
- very light purple (RGB 237, 231, 246) = scenario toggle or control logic
- very light teal (RGB 224, 242, 241) = key KPI box
- very light orange (RGB 255, 243, 224) = provisional, review-needed, or caution
- very light red (RGB 255, 235, 238) = failed check or conflicting logic
- very light gray (RGB 242, 244, 247) = note, source field, helper label, or reference column

Borders:
- thin bottom border for column headers
- single top border for subtotals
- thicker top border for major totals and bottom-line metrics
- do not box every populated cell

6. PALETTE

Use muted colors only.

- header black: RGB 0, 0, 0
- primary navy: RGB 31, 49, 79
- secondary slate: RGB 91, 122, 153
- light gray: RGB 242, 244, 247
- input yellow: RGB 255, 249, 196
- control purple: RGB 237, 231, 246
- KPI teal: RGB 224, 242, 241
- caution orange: RGB 255, 243, 224
- error red: RGB 255, 235, 238
- pass green: RGB 232, 245, 233

7. NUMBER AND DATE FORMATS

- show zeros as -
- show negatives in red parentheses
- percentages: 0.0% (one decimal) unless more precision is truly needed
- multiples: 0.0x
- whole numbers for unit counts and most operating counts
- do not mix currencies in one schedule without a clear label
- annual headers: 2026, 2027, 2028
- monthly headers: Jan-26, Feb-26
- milestone dates: dd-mmm-yy or mmm-yy
- units must be visible in every block header (e.g., USD mm, units, cost per unit, hours, days, etc.)

Number formatting safety:
- only apply number formats to cells whose values are truly numeric (int or float)
- range values stored as text (e.g., "5-35", "30-38", "<1") must be left completely untouched
- when converting text representations of numbers to actual numbers, verify the string contains no embedded dashes (other than a leading negative sign), letters, or special characters before converting
- if there is any ambiguity, leave the value as text rather than risk changing its meaning

8. TAB NAMING AND ORDER

- sentence case for every tab name
- no underscores
- plain English; avoid unnecessary abbreviations
- standard abbreviations like NPV, FCF, Capex are acceptable when they improve clarity or stay within Excel's 31-character tab name limit
- Excel tab names cannot contain a forward slash; use "and" or a hyphen instead
- number tabs so the first digit indicates the workbook group
- each group starts with a .0 divider tab immediately before its working tabs
- do not insert unrelated tabs inside a group
- scratch tabs go at the far right, prefixed with X or Z; remove before sharing

9. TAB FAMILY COLORS

Use tab colors only to identify major workbook groups. Do not assign every tab a different color.

- assign one muted color per logical group of tabs
- all working tabs within the same group share the same tab color
- the .0 divider tab uses the same color as the working tabs in that group
- keep the total number of distinct tab colors small; one per major workbook section is enough
- do not use bright or saturated tab colors

10. DIVIDER TAB STYLE

Each .0 tab is a visual section break.
- group title in a black-fill, white-bold band
- optional one-line description below in gray italic
- no formulas, no schedules, no other content

11. HEADER SYSTEM

Every working tab uses the same top structure:
- Row 1: tab title in black-fill, white-bold band through last active column
- Row 2: one-line purpose statement, gray italic, white fill
- Row 3: scenario, currency, unit basis, time basis in gray (or blank spacer row with white fill)
- Row 4: column headers in light gray subsection fill (RGB 242, 244, 247) with dark bold text and thin bottom border
- Row 5 onward: content begins

Column header row clarification:
- the column header row (field names like "Agency", "Vessel Class", etc.) uses the gray subsection style, not the black section header style
- using black fill for both the title band and the column headers causes them to visually merge into one undifferentiated block; the gray fill creates clear separation
- auto-filters, when used, should be anchored to this column header row (row 4), not the title band or purpose line

Rules:
- all header text in Arial 8
- left-align titles and purpose text
- keep the purpose line to one concise sentence
- avoid merged cells in the model body; limit merges to divider tabs or presentation-only title bands if used at all

12. SECTION AND SUBSECTION HEADERS

Major section header:
- black fill, white bold text
- spans through last active column
- one blank row above
- a typical working tab should have no more than two or three black section headers (the Row 1 title band does not count)

Subsection header:
- light gray fill (RGB 242, 244, 247) only; no tinted fills
- dark bold text
- spans through last active column
- when in doubt between a section header and a subsection header, use a subsection header

13. FILL EXTENT AND BLEED PREVENTION

Header and subsection bands:
- fill every cell through the last active column
- never fill only the label cell and leave the rest of the row empty

Explicit fill rule:
- at 10.0 row height, cells with no fill are transparent and will visually bleed into adjacent rows
- a cell with no fill sitting below a black title band will let the black bleed through, making white text appear to float on an unintended black background in the row below
- every cell through the last active column on every row must carry an explicit fill
- if a cell is not inside an accent box, header band, or tinted region, it must be set to explicit white fill
- never leave a cell without a fill assignment; "no fill" and "white fill" are not the same thing at this row height
- when writing a row that mixes fills (for example, white labels with yellow input cells), set the entire row to white first, then overwrite specific cells with the accent fill
- this white-first-then-accent pattern prevents any gap where a transparent cell could let color bleed through from the row above or below

Accent boxes (KPI teal, input yellow, control purple, caution orange, error red):
- must form complete rectangles with no gaps inside
- cells immediately outside the box on the same row carry explicit white fill

Separator rows:
- one blank row above and below any accent-filled box
- separator rows carry explicit white fill through the active width

14. LABEL HIERARCHY AND INDENTATION

- major section label: bold, no indent
- subcategory: normal or bold, one indent
- detailed line item: normal, two indents
- memo or note line: gray or italic
- subtotal: bold plus thin top border
- total: bold plus thicker top border

Alignment:
- row labels left aligned
- numbers right aligned
- dates centered or right aligned consistently

15. INPUT BLOCK RULES

- compact, clearly separated from the calculation body
- label on the left, assumption on the right
- blue text in every numeric cell whose value was typed by a human
- blue italic for any typed-in percentage
- text labels in input blocks remain black even when hand-entered
- light yellow fill for user-edit cells
- source note immediately adjacent if externally sourced
- one assumption per row
- never bury assumptions inside formulas
- if a control lives on a central control panel tab, show a green linked reference elsewhere rather than a second blue hardcode

16. SIGN CONVENTIONS

- detailed cost-build schedules can show costs as positive values
- formal income statement and cash flow exhibits should use one consistent outflow convention
- do not switch sign conventions within the same exhibit

17. FORMULA TRANSPARENCY

- keep input rows visually distinct from formula rows
- avoid embedded hardcodes in formulas
- use helper rows instead of unreadable formulas
- keep formula patterns consistent across time periods
- do not hide logic with white-font cells
- label plugs or balancing items explicitly

18. OUTLINE GROUPING

- dense detail can be grouped under visible summaries
- output and statement tabs should be expanded by default
- do not hide key assumptions, final answers, or quality checks
- if helper rows are hidden, visible summaries must still be understandable

19. SOURCE DOCUMENTATION

- every external research input should have a source and date in a source column or note
- every adopted model input should trace back to external research, internal benchmarks, management instruction, or internal assumption
- source text should be visually secondary (gray)
- research-heavy tabs should show confidence levels

20. NOTES AND CALLOUTS

- use notes to explain margin definitions, modeling simplifications, normalization choices, or where management guidance overrode a benchmark
- because row height is universal and text wrap is never used, long notes do not belong in the main model body
- prefer short one-line notes in a gray note column, or cell comments, or a dedicated readme or source log tab
- note boxes: light gray fill, dark gray text, Arial 8, concise wording

21. QA CHECK STYLING

- PASS = green fill
- FAIL = light red fill plus bold text
- WARNING = orange fill
- no ambiguous formatting for binary checks
- failed checks should never blend into the model body

22. CHART RULES

If charts are used:
- 2D only
- white background
- no shadows, gradients, or 3D
- minimal gridlines
- left-aligned title
- direct labels preferred over oversized legends
- match the workbook palette
- do not add a chart unless it adds clarity beyond the table

23. SHARE-READY CHECKLIST

Before sharing, confirm:
- tab order follows numbered group structure with .0 dividers
- tab names are sentence case, no underscores, plain English
- Arial 8 only, everywhere
- every row uses universal row height of 10.0
- gridlines hidden on every tab
- no frozen panes anywhere
- no text wrap on any cell
- every cell through the last active column carries an explicit fill; no transparent cells
- all percentage cells are italicized regardless of font color
- all hardcoded numeric values are blue; hand-entered text labels remain black
- blue, black, green, red, and gray conventions are consistent
- zeros show as -
- negatives show as red parentheses
- accent boxes are bounded and separated from adjacent bands
- source notes exist for key external inputs
- no loose tabs, orphan notes, or leftover formatting artifacts

24. OPENPYXL AND SCRIPTING IMPLEMENTATION NOTES

When building or maintaining this workbook programmatically with openpyxl, the following rules prevent common failures that are invisible in Python but break the file when opened in Excel.

Color codes must use 8-character ARGB with FF alpha prefix:
- openpyxl stores 6-character hex like "000000" as "00000000" where the leading "00" is the alpha channel
- Excel reads alpha "00" as fully transparent, so a black fill specified as "000000" renders as invisible
- always use "FF000000" for black, "FFFFFFFF" for white, "FFF2F4F7" for light gray, and so on
- this is the most common cause of missing header bands and invisible title rows

Removing frozen panes requires replacing the entire SheetView:
- setting ws.freeze_panes = None removes the freeze but leaves orphaned pane and selection XML elements
- Excel flags these as corrupt content and shows the "we found a problem" repair dialog on open
- the fix is to replace ws.views with a fresh SheetViewList containing a clean SheetView object
- example: ws.views = SheetViewList(); ws.views.sheetView.append(SheetView(showGridLines=False, workbookViewId=0))

Auto-filter cleanup must use a fresh AutoFilter object, not None:
- setting ws.auto_filter.ref = None writes an invalid empty filter element into the XML
- this also triggers the Excel repair dialog on open
- to clear an existing auto-filter, assign ws.auto_filter = AutoFilter() before reassigning to the correct range
- after inserting header system rows, auto-filters must be explicitly reassigned to the new column header row because they do not shift automatically

Case-insensitive sheet renaming:
- openpyxl treats sheet names as case-insensitive, so renaming "Class Hierarchy" to "Class hierarchy" is treated as a duplicate and silently becomes "Class hierarchy1"
- to rename with only a case change, first rename to a temporary placeholder name, then rename to the final name
- when renaming multiple sheets, rename all to temporary names first, then all to final names, to avoid any collision

Row insertion and downstream references:
- when inserting header system rows at the top of a sheet, all existing cell data shifts down but auto-filters, named ranges, and print areas do not shift automatically
- after insertion, verify and reassign auto-filters to the correct row
- if the column header row was originally row 1 and you insert 3 rows above it, the headers move to row 4 but the auto-filter may remain anchored to row 1

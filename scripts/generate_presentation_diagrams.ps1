Add-Type -AssemblyName System.Drawing

function Draw-RoundRect {
    param(
        [System.Drawing.Graphics]$Graphics,
        [System.Drawing.Pen]$Pen,
        [System.Drawing.Brush]$Brush,
        [float]$X,
        [float]$Y,
        [float]$W,
        [float]$H,
        [float]$R
    )
    $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $d = $R * 2
    $path.AddArc($X, $Y, $d, $d, 180, 90)
    $path.AddArc($X + $W - $d, $Y, $d, $d, 270, 90)
    $path.AddArc($X + $W - $d, $Y + $H - $d, $d, $d, 0, 90)
    $path.AddArc($X, $Y + $H - $d, $d, $d, 90, 90)
    $path.CloseFigure()
    if ($Brush) { $Graphics.FillPath($Brush, $path) }
    if ($Pen) { $Graphics.DrawPath($Pen, $path) }
    $path.Dispose()
}

function New-Canvas {
    param([int]$Width, [int]$Height, [string]$Title, [string]$Subtitle)
    $bmp = [System.Drawing.Bitmap]::new($Width, $Height)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear([System.Drawing.Color]::FromArgb(247, 248, 244))

    $titleFont = [System.Drawing.Font]::new("Segoe UI", 28, [System.Drawing.FontStyle]::Bold)
    $subFont = [System.Drawing.Font]::new("Segoe UI", 12, [System.Drawing.FontStyle]::Regular)
    $titleBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(31, 41, 55))
    $subBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(92, 102, 112))
    $g.DrawString($Title, $titleFont, $titleBrush, 40, 24)
    $g.DrawString($Subtitle, $subFont, $subBrush, 44, 70)
    $titleFont.Dispose()
    $subFont.Dispose()
    $titleBrush.Dispose()
    $subBrush.Dispose()

    return @{ Bitmap = $bmp; Graphics = $g }
}

function Draw-Box {
    param(
        [System.Drawing.Graphics]$Graphics,
        [float]$X,
        [float]$Y,
        [float]$W,
        [float]$H,
        [string]$Title,
        [string]$Body,
        [System.Drawing.Color]$FillColor,
        [System.Drawing.Color]$BorderColor
    )
    $fill = [System.Drawing.SolidBrush]::new($FillColor)
    $pen = [System.Drawing.Pen]::new($BorderColor, 2)
    Draw-RoundRect -Graphics $Graphics -Pen $pen -Brush $fill -X $X -Y $Y -W $W -H $H -R 16
    $titleFont = [System.Drawing.Font]::new("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
    $bodyFont = [System.Drawing.Font]::new("Segoe UI", 10, [System.Drawing.FontStyle]::Regular)
    $titleBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(36, 42, 48))
    $bodyBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(80, 88, 96))
    $Graphics.DrawString($Title, $titleFont, $titleBrush, [float]($X + 14), [float]($Y + 10))
    $rect = [System.Drawing.RectangleF]::new([float]($X + 14), [float]($Y + 42), [float]($W - 28), [float]($H - 50))
    $fmt = [System.Drawing.StringFormat]::new()
    $fmt.Trimming = [System.Drawing.StringTrimming]::Word
    $fmt.FormatFlags = [System.Drawing.StringFormatFlags]::LineLimit
    $Graphics.DrawString($Body, $bodyFont, $bodyBrush, $rect, $fmt)
    $fill.Dispose()
    $pen.Dispose()
    $titleFont.Dispose()
    $bodyFont.Dispose()
    $titleBrush.Dispose()
    $bodyBrush.Dispose()
    $fmt.Dispose()
}

function Draw-Arrow {
    param(
        [System.Drawing.Graphics]$Graphics,
        [float]$X1,
        [float]$Y1,
        [float]$X2,
        [float]$Y2,
        [System.Drawing.Color]$Color
    )
    $pen = [System.Drawing.Pen]::new($Color, 3)
    $pen.CustomEndCap = [System.Drawing.Drawing2D.AdjustableArrowCap]::new(6, 8, $true)
    $Graphics.DrawLine($pen, $X1, $Y1, $X2, $Y2)
    $pen.Dispose()
}

function Draw-Text {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [float]$X,
        [float]$Y,
        [int]$Size = 10,
        [bool]$Bold = $false
    )
    $style = if ($Bold) { [System.Drawing.FontStyle]::Bold } else { [System.Drawing.FontStyle]::Regular }
    $font = [System.Drawing.Font]::new("Segoe UI", $Size, $style)
    $brush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(88, 95, 99))
    $Graphics.DrawString($Text, $font, $brush, $X, $Y)
    $font.Dispose()
    $brush.Dispose()
}

function Save-Canvas {
    param($Canvas, [string]$Path)
    $Canvas.Bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $Canvas.Graphics.Dispose()
    $Canvas.Bitmap.Dispose()
}

$blue = [System.Drawing.Color]::FromArgb(221, 236, 252)
$blueB = [System.Drawing.Color]::FromArgb(70, 122, 179)
$green = [System.Drawing.Color]::FromArgb(224, 242, 230)
$greenB = [System.Drawing.Color]::FromArgb(79, 145, 102)
$amber = [System.Drawing.Color]::FromArgb(251, 240, 214)
$amberB = [System.Drawing.Color]::FromArgb(189, 145, 47)
$red = [System.Drawing.Color]::FromArgb(249, 226, 225)
$redB = [System.Drawing.Color]::FromArgb(186, 89, 84)
$gray = [System.Drawing.Color]::FromArgb(233, 236, 239)
$grayB = [System.Drawing.Color]::FromArgb(121, 129, 140)
$purple = [System.Drawing.Color]::FromArgb(235, 229, 248)
$purpleB = [System.Drawing.Color]::FromArgb(118, 94, 176)
$arrow = [System.Drawing.Color]::FromArgb(67, 78, 92)

$docs = "C:\Users\yusBug\Desktop\Powercoders\greenleaf-ai-assistant-bern-2026\docs"

# 1. System Context
$c = New-Canvas 1600 900 "Beat-Bot System Context" "Presentation view of users, core app, external services, and source data"
$g = $c.Graphics
Draw-Box $g 90 190 240 120 "Employees" "Ask handbook, holiday, and expense questions." $blue $blueB
Draw-Box $g 90 380 240 120 "Admins" "Review behavior, quality, and operational outcomes." $blue $blueB
Draw-Box $g 440 280 280 150 "Beat-Bot Web App" "Internal policy assistant with policy-first routing, retrieval, and safe refusals." $gray $grayB
Draw-Box $g 850 120 260 120 "OIDC Provider" "Authentication provider. Final choice still requires clarification." $purple $purpleB
Draw-Box $g 850 290 260 120 "OpenAI API" "LLM generation and constrained helper tasks." $purple $purpleB
Draw-Box $g 850 460 260 120 "PostgreSQL + pgvector" "Knowledge storage, chunk metadata, embeddings." $green $greenB
Draw-Box $g 850 630 260 120 "Approved Sources" "Handbook, stakeholder briefing, and holiday CSV." $green $greenB
Draw-Arrow $g 330 250 440 325 $arrow
Draw-Arrow $g 330 440 440 385 $arrow
Draw-Arrow $g 720 335 850 180 $arrow
Draw-Arrow $g 720 335 850 350 $arrow
Draw-Arrow $g 720 355 850 520 $arrow
Draw-Arrow $g 720 375 850 690 $arrow
Draw-Text $g "Uses login" 760 230
Draw-Text $g "Uses LLM/helper calls" 735 305
Draw-Text $g "Reads / writes knowledge" 735 460
Draw-Text $g "Uses approved content" 740 610
Save-Canvas $c (Join-Path $docs "system-context-diagram.png")

# 2. High-Level Architecture
$c = New-Canvas 1700 950 "Beat-Bot High-Level Architecture" "Policy-first RAG architecture for MVP"
$g = $c.Graphics
Draw-Box $g 80 180 250 120 "Next.js Frontend" "Chat UI, source display, refusal and redirect rendering." $blue $blueB
Draw-Box $g 420 180 250 120 "Auth Module" "Identity validation and role resolution." $purple $purpleB
Draw-Box $g 760 180 250 120 "Classification" "Hybrid routing: deterministic first, constrained helper fallback." $amber $amberB
Draw-Box $g 1100 160 280 160 "Policy Engine" "Expense, holiday, security, and misconduct routing rules." $red $redB
Draw-Box $g 420 430 250 120 "Retrieval Service" "Section-aware search over approved sources." $green $greenB
Draw-Box $g 760 430 250 120 "Answer Generation" "Evidence-backed explanations only." $green $greenB
Draw-Box $g 1100 430 280 120 "Response Templates" "Clarification, refusal, redirect, deterministic outcomes." $amber $amberB
Draw-Box $g 1450 305 180 120 "Validator" "Checks output structure and safety." $amber $amberB
Draw-Box $g 760 690 250 120 "OpenAI Helper Services" "Classification fallback, translation, future speech-to-text." $purple $purpleB
Draw-Box $g 1100 690 280 120 "PostgreSQL + pgvector" "Chunks, metadata, embeddings." $green $greenB
Draw-Arrow $g 330 240 420 240 $arrow
Draw-Arrow $g 670 240 760 240 $arrow
Draw-Arrow $g 1010 240 1100 240 $arrow
Draw-Arrow $g 1240 320 1240 430 $arrow
Draw-Arrow $g 1380 490 1450 365 $arrow
Draw-Arrow $g 1010 490 1100 490 $arrow
Draw-Arrow $g 670 490 760 490 $arrow
Draw-Arrow $g 545 300 545 430 $arrow
Draw-Arrow $g 1140 320 545 430 $arrow
Draw-Arrow $g 885 550 885 690 $arrow
Draw-Arrow $g 1240 550 1240 690 $arrow
Draw-Text $g "User request" 355 205
Draw-Text $g "Identity / role" 695 205
Draw-Text $g "Routing labels" 1035 205
Draw-Text $g "Policy-first branch" 1145 360
Draw-Text $g "Supported Q&A path" 710 400
Save-Canvas $c (Join-Path $docs "high-level-architecture-diagram.png")

# 2A. New High-Level System Architecture
$c = New-Canvas 1800 980 "High-Level System Architecture" "LLM-first architecture with retrieval, validation, and safe fallback"
$g = $c.Graphics
Draw-Box $g 80 210 240 120 "Next.js Frontend" "Chat UI, login, source display, and history views." $blue $blueB
Draw-Box $g 390 210 230 120 "FastAPI API" "Receives /ask, orchestrates backend flow, returns final response." $gray $grayB
Draw-Box $g 690 110 240 120 "Auth + Role Access" "Login/session handling and DB-backed Employee/Admin authorization." $purple $purpleB
Draw-Box $g 690 320 240 120 "Retrieval Layer" "Finds relevant approved chunks and citation metadata." $green $greenB
Draw-Box $g 1000 210 250 120 "OpenAI LLM" "Interprets the question and returns a structured draft response." $purple $purpleB
Draw-Box $g 1320 110 260 120 "Validator Layer" "Schema, citation, disclosure, consistency, and response-type checks." $amber $amberB
Draw-Box $g 1320 320 260 120 "Retry / Safe Fallback" "Retries once when useful or returns refusal, redirect, or verification failure." $amber $amberB
Draw-Box $g 1650 210 110 120 "Audit" "Stores outcomes." $gray $grayB
Draw-Box $g 690 570 240 130 "PostgreSQL + pgvector" "Users, roles, chats, messages, sources, chunk metadata, embeddings." $green $greenB
Draw-Box $g 1000 570 250 130 "Approved Sources" "Handbook, stakeholder briefing, holiday CSV." $green $greenB

Draw-Arrow $g 320 270 390 270 $arrow
Draw-Arrow $g 620 235 690 170 $arrow
Draw-Arrow $g 620 300 690 380 $arrow
Draw-Arrow $g 930 270 1000 270 $arrow
Draw-Arrow $g 1250 240 1320 170 $arrow
Draw-Arrow $g 1250 300 1320 380 $arrow
Draw-Arrow $g 1580 270 1650 270 $arrow
Draw-Arrow $g 810 440 810 570 $arrow
Draw-Arrow $g 1125 440 1125 570 $arrow
Draw-Arrow $g 1705 330 1705 570 $arrow

Draw-Text $g "login + ask flow" 330 235
Draw-Text $g "identity / authorization" 630 120
Draw-Text $g "grounding context" 730 470
Draw-Text $g "structured draft" 1065 175
Draw-Text $g "pass / fail" 1365 245
Draw-Text $g "validator and chat metadata" 1540 520

Draw-Text $g "Boundary rules:" 80 780 16 $true
Draw-Text $g "- LLM does not access the database directly" 100 820 13
Draw-Text $g "- Backend owns auth, role mapping, and release decisions" 100 855 13
Draw-Text $g "- Only minimum necessary context is sent to the model" 100 890 13

Save-Canvas $c (Join-Path $docs "high-level-system-architecture-diagram.png")

# 3. Request Flow
$c = New-Canvas 1800 980 "Beat-Bot End-to-End Request Flow" "How one user question moves through the system"
$g = $c.Graphics
$steps = @(
    @{ X = 70; Y = 260; W = 180; H = 110; T = "1. User Question"; B = "Employee or Admin submits a question in the UI."; C = $blue; CB = $blueB },
    @{ X = 300; Y = 260; W = 180; H = 110; T = "2. Validate"; B = "API validates request format and session."; C = $gray; CB = $grayB },
    @{ X = 530; Y = 260; W = 180; H = 110; T = "3. Classify"; B = "Hybrid classification assigns domain and routing path."; C = $amber; CB = $amberB },
    @{ X = 760; Y = 260; W = 180; H = 110; T = "4. Policy Route"; B = "Policy engine chooses decision, refusal, redirect, or Q&A path."; C = $red; CB = $redB },
    @{ X = 1010; Y = 140; W = 220; H = 110; T = "5A. Clarify / Refuse / Redirect"; B = "Template-based controlled response path."; C = $amber; CB = $amberB },
    @{ X = 1010; Y = 380; W = 220; H = 110; T = "5B. Retrieval"; B = "Relevant chunks are fetched from approved sources."; C = $green; CB = $greenB },
    @{ X = 1280; Y = 380; W = 220; H = 110; T = "6. Generate"; B = "LLM produces evidence-backed explanation."; C = $green; CB = $greenB },
    @{ X = 1550; Y = 260; W = 180; H = 110; T = "7. Validate Response"; B = "Schema, citations, and safety checks run."; C = $amber; CB = $amberB },
    @{ X = 1550; Y = 560; W = 180; H = 110; T = "8. Audit"; B = "Routing, rules, evidence, and output are logged."; C = $gray; CB = $grayB }
)
foreach ($s in $steps) { Draw-Box $g $s.X $s.Y $s.W $s.H $s.T $s.B $s.C $s.CB }
Draw-Arrow $g 250 315 300 315 $arrow
Draw-Arrow $g 480 315 530 315 $arrow
Draw-Arrow $g 710 315 760 315 $arrow
Draw-Arrow $g 940 280 1010 215 $arrow
Draw-Arrow $g 940 350 1010 435 $arrow
Draw-Arrow $g 1230 435 1280 435 $arrow
Draw-Arrow $g 1230 215 1550 315 $arrow
Draw-Arrow $g 1500 435 1550 345 $arrow
Draw-Arrow $g 1640 370 1640 560 $arrow
Draw-Text $g "deterministic / safety path" 1010 95
Draw-Text $g "supported handbook explanation path" 1040 515
Draw-Text $g "all outcomes" 1360 300
Save-Canvas $c (Join-Path $docs "request-flow-diagram.png")

# 4. Expense Decision Flow
$c = New-Canvas 1600 1000 "Expense Decision Flow" "How the MVP decides whether an expense question can be answered"
$g = $c.Graphics
Draw-Box $g 610 80 360 100 "Expense Question" "Example: Can I expense my lunch receipt?" $blue $blueB
Draw-Box $g 610 220 360 100 "Enough decision data?" "Amount, person count, alcohol status, and external-client presence." $amber $amberB
Draw-Box $g 120 410 300 100 "Clarification Template" "Ask the user for missing fields before any decision." $amber $amberB
Draw-Box $g 610 410 360 100 "Alcohol included?" "Deterministic expense rule check." $red $redB
Draw-Box $g 1100 410 300 100 "Above 35 CHF per person?" "Deterministic expense rule check." $red $redB
Draw-Box $g 610 600 360 100 "External client present?" "If unknown, ask follow-up or avoid final approval-style answer." $amber $amberB
Draw-Box $g 120 790 300 100 "Reject" "Alcohol or over-limit scenario -> policy-based rejection." $red $redB
Draw-Box $g 610 790 360 100 "Needs Clarification" "If client presence or attendee count is still unclear." $amber $amberB
Draw-Box $g 1100 790 300 100 "Potentially Allowed" "Only if all required conditions are satisfied; explain with citation." $green $greenB
Draw-Arrow $g 790 180 790 220 $arrow
Draw-Arrow $g 610 270 420 460 $arrow
Draw-Arrow $g 790 320 790 410 $arrow
Draw-Text $g "No" 500 355 12 $true
Draw-Text $g "Yes" 810 355 12 $true
Draw-Arrow $g 970 460 1100 460 $arrow
Draw-Arrow $g 610 460 420 840 $arrow
Draw-Text $g "Alcohol = yes" 420 620
Draw-Arrow $g 1250 510 1250 790 $arrow
Draw-Arrow $g 1100 460 970 460 $arrow
Draw-Text $g "No" 1020 425 12 $true
Draw-Text $g "Yes" 1270 650 12 $true
Draw-Arrow $g 790 510 790 600 $arrow
Draw-Arrow $g 790 700 790 790 $arrow
Draw-Arrow $g 970 650 1100 840 $arrow
Draw-Text $g "Known and valid" 805 730
Draw-Text $g "Still unclear" 980 730
Save-Canvas $c (Join-Path $docs "expense-decision-flow-diagram.png")

# 5. Security / Guardrail Diagram
$c = New-Canvas 1700 980 "Security and Guardrail Logic" "What the bot may answer, refuse, or redirect"
$g = $c.Graphics
Draw-Box $g 650 90 380 100 "Incoming Question" "The system classifies the topic before retrieval or generation begins." $blue $blueB
Draw-Box $g 150 260 300 120 "Supported Policy Q&A" "Handbook-based questions with safe scope and good evidence." $green $greenB
Draw-Box $g 520 260 320 120 "Sensitive IT / Access Question" "Passwords, MAC-registration detail, internal technical access information." $red $redB
Draw-Box $g 940 260 320 120 "Misconduct / Sensitive Conduct" "Harassment, bullying, whistleblowing." $red $redB
Draw-Box $g 1310 260 240 120 "Weak Evidence / Unknown" "Question cannot be answered safely." $amber $amberB
Draw-Box $g 150 500 300 120 "Answer with Citation" "Use retrieval plus generation or deterministic explanation." $green $greenB
Draw-Box $g 520 500 320 120 "Refusal Template" "Do not disclose, provide safe boundary message." $amber $amberB
Draw-Box $g 940 500 320 120 "Redirect Template" "Send user to the ombudsman or correct process." $amber $amberB
Draw-Box $g 1310 500 240 120 "Fallback / Clarify" "Ask follow-up or refuse when evidence is insufficient." $amber $amberB
Draw-Box $g 520 730 500 140 "Core Rule" "Source presence does not equal disclosure permission. Even if a source contains a sensitive detail, the bot may still need to refuse." $gray $grayB
Draw-Arrow $g 840 190 300 260 $arrow
Draw-Arrow $g 840 190 680 260 $arrow
Draw-Arrow $g 840 190 1100 260 $arrow
Draw-Arrow $g 840 190 1430 260 $arrow
Draw-Arrow $g 300 380 300 500 $arrow
Draw-Arrow $g 680 380 680 500 $arrow
Draw-Arrow $g 1100 380 1100 500 $arrow
Draw-Arrow $g 1430 380 1430 500 $arrow
Draw-Arrow $g 680 620 740 730 $arrow
Draw-Arrow $g 1100 620 980 730 $arrow
Draw-Text $g "allowed path" 250 420
Draw-Text $g "refuse" 640 420
Draw-Text $g "redirect" 1060 420
Draw-Text $g "safe fallback" 1380 420
Save-Canvas $c (Join-Path $docs "security-guardrail-diagram.png")

# 6. Ask Flow Sequence
$c = New-Canvas 1900 1040 "Ask Flow Sequence" "LLM-first request flow with backend-controlled validation and persistence"
$g = $c.Graphics

Draw-Box $g 60 150 170 90 "1. User" "Sends a question from the UI." $blue $blueB
Draw-Box $g 280 150 190 90 "2. Frontend" "Calls POST /ask with session info." $blue $blueB
Draw-Box $g 520 150 190 90 "3. API" "Validates request and orchestrates the flow." $gray $grayB
Draw-Box $g 760 70 210 90 "4. Auth Service" "Loads current user and role mapping." $purple $purpleB
Draw-Box $g 760 230 210 90 "5. Retrieval" "Fetches relevant source chunks and citation metadata." $green $greenB
Draw-Box $g 1030 150 230 90 "6. OpenAI API" "Returns a structured draft response." $purple $purpleB
Draw-Box $g 1320 70 220 90 "7. Validators" "Schema, citation, disclosure, consistency, response type." $amber $amberB
Draw-Box $g 1320 230 220 90 "8. Fallbacks" "Retry once or build a safe fallback." $amber $amberB
Draw-Box $g 1600 150 210 90 "9. Response Formatter" "Formats the validated draft or fallback." $gray $grayB
Draw-Box $g 760 420 210 90 "10. PostgreSQL" "Users, roles, chats, messages, sources, embeddings." $green $greenB
Draw-Box $g 1320 420 220 90 "11. Audit / History" "Persists chat history, validator results, metadata." $gray $grayB

Draw-Arrow $g 230 195 280 195 $arrow
Draw-Arrow $g 470 195 520 195 $arrow
Draw-Arrow $g 615 150 820 115 $arrow
Draw-Arrow $g 615 240 820 275 $arrow
Draw-Arrow $g 970 195 1030 195 $arrow
Draw-Arrow $g 1260 175 1320 115 $arrow
Draw-Arrow $g 1260 215 1320 275 $arrow
Draw-Arrow $g 1540 195 1600 195 $arrow
Draw-Arrow $g 1705 240 1430 420 $arrow
Draw-Arrow $g 860 320 860 420 $arrow

Draw-Text $g "session + request" 350 165
Draw-Text $g "user + role lookup" 690 60
Draw-Text $g "grounding context" 705 345
Draw-Text $g "structured draft" 1085 120
Draw-Text $g "pass or fail" 1350 175
Draw-Text $g "retry / safe fallback" 1328 335
Draw-Text $g "persist history + audit trail" 1445 455

Draw-Text $g "Important boundaries:" 60 620 16 $true
Draw-Text $g "- LLM has no direct database access" 80 660 13
Draw-Text $g "- Backend owns identity, role mapping, and authorization" 80 695 13
Draw-Text $g "- Only minimum necessary context is sent to the LLM" 80 730 13
Draw-Text $g "- Only validated drafts or safe fallbacks reach the user" 80 765 13

Save-Canvas $c (Join-Path $docs "ask-flow-sequence-diagram.png")

Get-ChildItem $docs -Filter "*diagram*.png" | Select-Object -ExpandProperty FullName

from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.learning.models import (
    Cohort, Week, Topic, ReferenceMaterial, Tool, ToolFeature,
    Assignment, RubricCriterion
)


WEEKS = [
    # ------------------------------------------------------------------
    # WEEK 1
    # ------------------------------------------------------------------
    {
        'number': 1,
        'title': 'Orientation, Diagnostic and Comparative Curriculum Literacy',
        'week_description': '''<h3>What this week is about</h3>
<p>This opening week sets the foundation for the whole certificate. You will orient yourself to the platform and its assessment rubric, complete a diagnostic self-assessment of your current digital-pedagogy practice, and start a personal Problem of Practice journal that you will keep across all thirteen weeks.</p>
<p>You will also compare your subject across five curricula, CBE, IGCSE, IB, BNC and American, to see how the same learning goals appear under different names. The aim is not to memorise any single curriculum but to build a translation table you will reuse in every later week.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Complete a baseline self-assessment of your practice</li>
<li>Map your subject across five curricula</li>
<li>Keep a Problem of Practice journal through the certificate</li>
</ul>''',
        'topics': [
            {
                'title': 'Comparative Curriculum Reference: CBE, IGCSE, IB, BNC, American',
                'description': '<p>All five curricula organise around the same six domains: language and literacy, mathematics, sciences, humanities and social studies, digital literacy and ICT, and creative and physical education. The names differ, but the underlying question is identical: what should a learner know and be able to do by a given point.</p>',
                'materials': [
                    {'title': 'KICD, Kenya Institute of Curriculum Development', 'content': '<p>Official source for CBE strands and sub-strands.</p>', 'url': 'https://kicd.ac.ke/'},
                    {'title': 'Cambridge International Syllabuses', 'content': '<p>IGCSE and AS/A Level syllabuses with assessment objectives.</p>', 'url': 'https://www.cambridgeinternational.org/'},
                    {'title': 'IB Organization', 'content': '<p>PYP, MYP and DP frameworks, Approaches to Learning and Learner Profile.</p>', 'url': 'https://www.ibo.org/'},
                    {'title': 'UK National Curriculum', 'content': '<p>Programmes of study by Key Stage.</p>', 'url': 'https://www.gov.uk/national-curriculum'},
                    {'title': 'Common Core State Standards', 'content': '<p>American standards for English and Mathematics.</p>', 'url': 'https://www.corestandards.org/'},
                ],
            },
        ],
        'tools': [
            {
                'name': 'Microsoft Word',
                'developer': 'Microsoft Corporation',
                'category': 'Productivity',
                'description': '''<h3>What it is</h3>
<p>Word is the standard word processor used across nearly every school system. Beyond typing, it is built for structured documents: automatic heading levels, tables of contents, tables, tracked feedback and mail merge.</p>
<h3>What it helps you achieve</h3>
<p>For this week, Word is your tool for the Curriculum Alignment Worksheet. It gives you a clean comparison table and it lets a colleague leave visible, reversible feedback via Track Changes, so the document improves over several drafts without anything being lost.</p>''',
                'website': 'https://www.microsoft.com/en-us/microsoft-365/word',
                'features': [
                    ('Styles and Headings', '<p>Consistent, navigable headings and an automatic table of contents.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a blank document.</li><li>On the Home tab, find the Styles gallery.</li><li>Type your heading, select it, click Heading 1 or Heading 2.</li><li>For an automatic table of contents, go to References, then Table of Contents.</li></ol>'),
                    ('Track Changes', '<p>Visible, reversible feedback from a peer reviewer.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the Review tab.</li><li>Click Track Changes.</li><li>Share the document.</li><li>Every edit appears as a coloured change you can accept or reject.</li></ol>'),
                    ('Tables', '<p>Structured grids for comparing curricula.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Insert, then Table.</li><li>Choose the rows and columns you need.</li><li>Type into each cell.</li><li>Apply a Table Style for readability.</li></ol>'),
                ],
            },
            {
                'name': 'Google Docs',
                'developer': 'Google',
                'category': 'Productivity',
                'description': '''<h3>What it is</h3>
<p>Google Docs is the free, browser-based equivalent to Word. Its standout feature is real-time collaboration: several people can type into the same document simultaneously, each cursor visible.</p>
<h3>What it helps you achieve</h3>
<p>Use Google Docs if you want to build the worksheet with a colleague in another location, or if your school already uses Google Workspace. It removes the back-and-forth of emailing files.</p>''',
                'website': 'https://docs.google.com/',
                'features': [
                    ('Real-time Co-editing', '<p>Several people editing the same document at once.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a Google Doc.</li><li>Click Share.</li><li>Add collaborators by email.</li><li>Each person\'s cursor appears in a distinct colour as they type.</li></ol>'),
                    ('Comment and Suggesting Mode', '<p>Structured feedback that can be accepted or rejected.</p>', '<p><strong>How to use:</strong></p><ol><li>Select the text.</li><li>Click Insert, then Comment, or press Ctrl+Alt+M.</li><li>Or switch to Suggesting mode from the dropdown in the top right.</li></ol>'),
                    ('Version History', '<p>See every past revision and restore any of them.</p>', '<p><strong>How to use:</strong></p><ol><li>Click File, then Version history, then See version history.</li><li>Click any timestamp to preview it.</li><li>Click Restore to roll back.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Curriculum Alignment Worksheet',
            'description': '''<h3>What this assignment is about</h3>
<p>The goal is to build a working translation table between your own curriculum and the other four in this course. This is not an academic essay. It is a document you will open again and again during the next twelve weeks, whenever a new tool or framework appears and you want to see how it lands in your classroom.</p>
<h3>The two tools you will use</h3>
<h4>Microsoft Word</h4>
<p>Word is the standard document editor for structured writing. It gives you heading styles that keep the document navigable, tables for the curriculum comparison, and Track Changes so a peer can review your draft and leave visible feedback. Use it if you are more comfortable with a desktop application.</p>
<h4>Google Docs</h4>
<p>Google Docs is the free, browser-based equivalent to Word. Its standout feature is real-time collaboration: several people can type into the same document at once. Use it if you want to work with a colleague at the same time, or if your school already relies on Google Workspace.</p>
<h3>The task</h3>
<ol>
<li>List the subject you teach and the grade level or levels.</li>
<li>Locate your subject\'s official documentation in your own curriculum: KICD for CBE, Cambridge International for IGCSE, the IB subject guide for IB, gov.uk for BNC, and Common Core or your state standards for American.</li>
<li>Identify the closest matching strand, objective, or standard in at least three other curricula. Use a table to line them up side by side.</li>
<li>Note one point of genuine difference between your curriculum and the others, not just different wording.</li>
<li>Write a short reflection at the bottom: how will you use this translation table in your own teaching this term?</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A single document, one to two pages, clean and well structured. The comparison table should be easy to read at a glance. The reflection should be specific, not generic. You will submit a shareable link, and a peer reviewer will score it against the rubric and leave feedback.</p>''',
            'prompt': '''<p>Produce a one-page or two-page Curriculum Alignment Worksheet. Include:</p>
<ul>
<li>A clear subject and grade-level identifier</li>
<li>A comparison table matching your subject to at least three other curricula</li>
<li>One genuine point of difference explained in your own words</li>
<li>A short personal reflection on how you will use the worksheet</li>
</ul>
<p>Submit a shareable link to the finished document. Ensure anyone with the link can view it.</p>''',
            'submission_type': 'link',
            'rubric': [
                ('Coverage', '<p>Your subject is compared against at least three other curricula.</p>', 20),
                ('Accuracy', '<p>Structures are correctly identified and named.</p>', 25),
                ('Genuine insight', '<p>The point of difference is substantive, not just wording.</p>', 25),
                ('Reflection quality', '<p>The personal teaching note is specific and actionable.</p>', 30),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 2
    # ------------------------------------------------------------------
    {
        'number': 2,
        'title': 'Learning Theory and Technology-Integration Frameworks',
        'week_description': '''<h3>What this week is about</h3>
<p>This is the conceptual heart of the certificate. You will work through six frameworks that underpin every later week: Bloom\'s Taxonomy, Gardner\'s Multiple Intelligences, TPACK, SAMR, Universal Design for Learning, and the Triple E Framework. None of them is a piece of software. Each is a lens for thinking about what makes technology use meaningful.</p>
<p>You will learn each framework, apply it to one of your own existing lessons, and see how the six pieces fit together: Bloom\'s and MI address the learner, TPACK and SAMR address the tool choice, UDL and Triple E address the design quality.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Explain each framework in plain language</li>
<li>Apply TPACK and SAMR to a real lesson</li>
<li>Use UDL and Triple E as design-quality checks</li>
</ul>''',
        'topics': [
            {
                'title': 'Bloom\'s Taxonomy (Revised)',
                'description': '<p>Six levels of cognitive demand: Remember, Understand, Apply, Analyze, Evaluate, Create. Used throughout this course to describe what a task actually asks of a learner.</p>',
                'materials': [{'title': 'Bloom\'s Taxonomy guide', 'content': '<p>Reference on the revised taxonomy from Vanderbilt University\'s Center for Teaching.</p>', 'url': 'https://cft.vanderbilt.edu/guides-sub-pages/blooms-taxonomy/'}],
            },
            {
                'title': 'Gardner\'s Theory of Multiple Intelligences',
                'description': '<p>Eight ways of processing and demonstrating understanding: Linguistic, Logical-Mathematical, Spatial, Bodily-Kinesthetic, Musical, Interpersonal, Intrapersonal, Naturalistic. Used here as a planning-variety checklist, not a fixed label.</p>',
                'materials': [{'title': 'Harvard Project Zero', 'content': '<p>The origin of the framework and current work on it.</p>', 'url': 'https://pz.harvard.edu/'}],
            },
            {
                'title': 'TPACK, Technological Pedagogical Content Knowledge',
                'description': '<p>Effective teaching with technology requires the intersection of Content, Pedagogy, and Technology knowledge. Before choosing any tool, state your content goal, then your pedagogical approach, then choose the technology that serves both.</p>',
                'materials': [{'title': 'TPACK.org', 'content': '<p>Official site of the framework by Mishra and Koehler.</p>', 'url': 'https://tpack.org/'}],
            },
            {
                'title': 'SAMR Model',
                'description': '<p>Substitution, Augmentation, Modification, Redefinition. A ladder for judging how meaningfully a tool changes a task. Not a demand to reach Redefinition every time, but a habit of asking the question.</p>',
                'materials': [{'title': 'Kathy Schrock\'s SAMR guide', 'content': '<p>Practical examples at each rung.</p>', 'url': 'https://www.schrockguide.net/samr.html'}],
            },
            {
                'title': 'Universal Design for Learning',
                'description': '<p>Design flexibility in from the start: multiple means of Engagement, Representation and Action and Expression. The content stays the same, the access points multiply.</p>',
                'materials': [{'title': 'CAST UDL Guidelines', 'content': '<p>The definitive framework and checkpoints.</p>', 'url': 'https://udlguidelines.cast.org/'}],
            },
            {
                'title': 'Triple E Framework',
                'description': '<p>Engage, Enhance, Extend. A tool-use check that asks whether the technology actually serves the learning goal, rather than just decorating the lesson.</p>',
                'materials': [{'title': 'Triple E Framework', 'content': '<p>Official site by Liz Kolb, University of Michigan.</p>', 'url': 'https://www.tripleeframework.com/'}],
            },
        ],
        'tools': [],
        'assignment': {
            'title': 'SAMR and TPACK Analysis of Your Lesson',
            'description': '''<h3>What this assignment is about</h3>
<p>You will take one lesson you already teach and analyse it through two frameworks: TPACK and SAMR. The purpose is to build the habit of asking, before you reach for a tool, whether the tool is actually serving the content and the pedagogy, and then asking how meaningfully the tool changes the task.</p>
<h3>The two frameworks you will use</h3>
<h4>TPACK</h4>
<p>TPACK says that good teaching with technology requires three kinds of knowledge held at once: Content (your subject), Pedagogy (how people learn and how to teach it), and Technology (what a given tool can do). None of the three is sufficient alone. Before choosing a tool, you state your content goal, then your pedagogical approach, then the tool that serves both.</p>
<h4>SAMR</h4>
<p>SAMR gives you four rungs to judge how much a tool is actually changing the task. Substitution means the tool replaces a non-digital task with no functional change. Augmentation means it replaces the task with a real functional improvement. Modification means the task itself is significantly redesigned. Redefinition means the tool enables an entirely new kind of task that had no non-digital equivalent. The bottom two rungs are Enhancement. The top two are Transformation.</p>
<h3>The task</h3>
<ol>
<li>Choose one lesson you currently teach.</li>
<li>Write the TPACK triad: three sentences stating your content goal, your pedagogical approach, and the technology you use. Be honest if the technology was chosen first and justified afterward.</li>
<li>Classify the lesson on the SAMR ladder. Justify the level with concrete evidence from your lesson, not your intention.</li>
<li>Suggest one concrete change that would move the lesson up one SAMR rung.</li>
<li>Write a short reflection on what the analysis revealed: was the tool chosen well, and could it be used more purposefully?</li>
</ol>
<h3>What a good submission looks like</h3>
<p>Between five hundred and eight hundred words. Clear structure. The TPACK triad stated as three clean sentences. The SAMR classification honest, even if the result is Substitution. The reflection should read like a teacher who is genuinely re-examining a lesson, not performing an analysis for the sake of it.</p>''',
            'prompt': '''<p>Submit a written analysis of one of your own lessons. Structure it as follows:</p>
<ul>
<li>Context: your subject, grade level, and lesson topic</li>
<li>TPACK triad: content, pedagogy, technology as three sentences</li>
<li>SAMR classification: which rung, and why, with concrete evidence</li>
<li>One concrete change to move up one rung</li>
<li>A short reflection on what the analysis revealed</li>
</ul>
<p>Submit a shareable link to the document.</p>''',
            'submission_type': 'link',
            'rubric': [
                ('TPACK triad clarity', '<p>Content, pedagogy and technology all clearly stated.</p>', 25),
                ('SAMR classification accuracy', '<p>The level is correctly identified with evidence.</p>', 30),
                ('Critical insight', '<p>The reflection goes beyond description to genuine analysis.</p>', 25),
                ('Structure and clarity', '<p>Well organised, easy to read.</p>', 20),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 3
    # ------------------------------------------------------------------
    {
        'number': 3,
        'title': 'Instructional and Learning Design',
        'week_description': '''<h3>What this week is about</h3>
<p>You will learn to design a lesson or unit by starting from the finish line. Backward Design and the ADDIE model are the two frameworks for this. Backward Design is for planning a single unit well. ADDIE is for building and improving materials over repeated cycles.</p>
<p>You will apply both to a real unit of your own and finish the week with a fully designed unit plan. This plan becomes the backbone of your capstone portfolio at the end of the course.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Design a unit starting from assessment evidence</li>
<li>Apply ADDIE to a lesson or training cycle</li>
<li>Write measurable learning objectives</li>
</ul>''',
        'topics': [
            {
                'title': 'Backward Design (Understanding by Design)',
                'description': '<p>Three stages, always in this order: identify desired results, determine acceptable evidence, plan learning experiences and tool choices. Assessment is designed before any activity is written.</p>',
                'materials': [{'title': 'Vanderbilt CFT, Understanding by Design', 'content': '<p>Overview of the Wiggins and McTighe framework.</p>', 'url': 'https://cft.vanderbilt.edu/guides-sub-pages/understanding-by-design/'}],
            },
            {
                'title': 'ADDIE Model',
                'description': '<p>Five phases, cyclical: Analyze, Design, Develop, Implement, Evaluate. Evaluate feeds back into Analyze for the next cycle.</p>',
                'materials': [{'title': 'instructionaldesign.org, ADDIE', 'content': '<p>The five-phase cycle in detail.</p>', 'url': 'https://www.instructionaldesign.org/models/addie/'}],
            },
        ],
        'tools': [
            {
                'name': 'Microsoft Excel',
                'developer': 'Microsoft Corporation',
                'category': 'Productivity',
                'description': '''<h3>What it is</h3>
<p>Excel is a spreadsheet application built on formulas and conditional formatting. Instead of a static grid of numbers, it recalculates the moment you change one value.</p>
<h3>What it helps you achieve</h3>
<p>For this week, Excel is your scope-and-sequence mapping tool. You will lay out your whole term\'s units across columns and rows, see the sequence at a glance, and spot gaps or duplications you would otherwise miss on paper.</p>''',
                'website': 'https://www.microsoft.com/en-us/microsoft-365/excel',
                'features': [
                    ('Formulas', '<p>Sum, average, and other calculations that update automatically.</p>', '<p><strong>How to use:</strong></p><ol><li>Click an empty cell.</li><li>Type =SUM(A1:A10) or =AVERAGE(A1:A10).</li><li>Press Enter.</li><li>Change any value in the range and the total updates.</li></ol>'),
                    ('Conditional Formatting', '<p>Automatic visual flags when a value crosses a threshold.</p>', '<p><strong>How to use:</strong></p><ol><li>Select the cells you want to monitor.</li><li>Home tab, Conditional Formatting, Highlight Cells Rules.</li><li>Choose Less Than and enter your threshold.</li><li>Pick a fill colour.</li></ol>'),
                    ('Charts', '<p>Visualise trends for staff or parent meetings.</p>', '<p><strong>How to use:</strong></p><ol><li>Select the data range.</li><li>Insert, then Chart.</li><li>Choose bar, line or pie.</li><li>Refine through the Chart Design tab.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Backward-Designed Unit Plan',
            'description': '''<h3>What this assignment is about</h3>
<p>You will take one upcoming unit of your own and design it from the finish line back. This is the single most important planning habit in the certificate. Every later week builds on it, and every capstone portfolio opens with a unit plan designed this way.</p>
<h3>The two frameworks you will use</h3>
<h4>Backward Design</h4>
<p>Backward Design asks you to start from the end. First you state the desired result: what should a learner understand or be able to do by the final lesson. Second, you determine acceptable evidence: what would prove they got there, decided before any activity is planned. Third, and only third, you plan the activities and tool choices that will produce that evidence. Most planning starts from activity and works forward; Backward Design flips the order, and the whole unit becomes more coherent as a result.</p>
<h4>ADDIE</h4>
<p>ADDIE is the framework for building and improving materials over time. Five phases: Analyze your learners, Design your approach, Develop the materials, Implement with real learners, Evaluate what happened and feed the findings back into Analyze for the next cycle. For a single unit plan, ADDIE gives you the structure to iterate: your first version is a draft, the second is informed by real classroom data.</p>
<h3>The task</h3>
<ol>
<li>Choose one upcoming unit, ideally two to four weeks long.</li>
<li>Write the desired result in one clear sentence. Include the Bloom\'s level of the objective.</li>
<li>Write the assessment evidence. What will learners produce, and what would make it excellent versus adequate? If you can, sketch a rubric.</li>
<li>Only then, plan the sequence of learning activities. Each activity should connect back to the desired result.</li>
<li>Check UDL: does each learner have at least two ways to access the content and at least two ways to demonstrate understanding?</li>
<li>Write a short reflection on the ADDIE cycle: what would you want to evaluate after the unit runs, and what might you change in the next cycle?</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A single document in a clean three-part structure: desired result, assessment evidence, learning activities. The activities should look purposeful rather than busy. The reflection should be honest about what you will not know until the unit runs. If your activities were designed first and the desired result was written afterward to justify them, that will be visible, and it will cost you marks.</p>''',
            'prompt': '''<p>Submit a fully backward-designed unit plan. Include:</p>
<ul>
<li>Desired result, stated in one clear sentence with the Bloom\'s level identified</li>
<li>Assessment evidence, including a rubric draft if possible</li>
<li>Learning activities, each connected back to the desired result</li>
<li>A UDL check: two access points and two demonstration points</li>
<li>A short reflection on what you would evaluate after the unit runs</li>
</ul>
<p>Submit a shareable link to the document.</p>''',
            'submission_type': 'link',
            'rubric': [
                ('Desired result', '<p>Clear, measurable, high-cognition objective.</p>', 25),
                ('Assessment evidence', '<p>Genuinely proves the desired result was reached.</p>', 25),
                ('Activity alignment', '<p>Activities lead directly to the evidence.</p>', 30),
                ('UDL differentiation', '<p>Multiple means of representation and expression.</p>', 20),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 4
    # ------------------------------------------------------------------
    {
        'number': 4,
        'title': 'Productivity and Documentation Mastery',
        'week_description': '''<h3>What this week is about</h3>
<p>Every tool in this week is software you have probably opened before, but likely not used to its full ability. You will learn Word, Excel, PowerPoint, Google Workspace, calendar habits, and digital notebooks at a professional standard, the level at which they genuinely save you time rather than adding admin.</p>
<p>You will finish the week with two real artifacts: a working digital gradebook and a professional lesson slide deck.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Use MS Office and Google Workspace at a professional standard</li>
<li>Build a gradebook with formulas and conditional formatting</li>
<li>Design a clean slide deck using Slide Master</li>
</ul>''',
        'topics': [],
        'tools': [
            {
                'name': 'Microsoft PowerPoint',
                'developer': 'Microsoft Corporation',
                'category': 'Productivity',
                'description': '''<h3>What it is</h3>
<p>PowerPoint builds slide-based presentations. It is the standard tool for direct instruction and learner presentation tasks.</p>
<h3>What it helps you achieve</h3>
<p>Two features change the quality of your decks almost instantly. The Slide Master makes every slide look consistent and professional without hand-formatting each one. Purposeful animation reveals information in a planned order, so you control the pace of a lesson rather than dumping a whole slide at once.</p>''',
                'website': 'https://www.microsoft.com/en-us/microsoft-365/powerpoint',
                'features': [
                    ('Slide Master', '<p>Set a consistent design once and it applies to every slide.</p>', '<p><strong>How to use:</strong></p><ol><li>Go to View, then Slide Master.</li><li>Edit fonts, colours and logo on the master slide.</li><li>Close Master View.</li><li>Every new slide inherits the design.</li></ol>'),
                    ('Purposeful Animation', '<p>Reveal information in a planned sequence.</p>', '<p><strong>How to use:</strong></p><ol><li>Select an object.</li><li>Open the Animations tab.</li><li>Choose Appear, Fade or Wipe.</li><li>Set Start to On Click or With Previous.</li></ol>'),
                    ('Export as Video', '<p>Repurpose a lesson deck as an asynchronous resource.</p>', '<p><strong>How to use:</strong></p><ol><li>File, then Export, then Create a Video.</li><li>Choose quality and timing.</li><li>Click Create Video.</li></ol>'),
                ],
            },
            {
                'name': 'Google Workspace for Education',
                'developer': 'Google',
                'category': 'Productivity',
                'description': '''<h3>What it is</h3>
<p>Google Workspace is the free cloud-based productivity suite: Docs, Sheets, Slides, plus Google Classroom as a lightweight course hub.</p>
<h3>What it helps you achieve</h3>
<p>The one feature Microsoft Office genuinely cannot match for free is real-time, simultaneous multi-person editing. Several students can type into the same document at once, each visible live. Google Classroom centralises assignments and communication for a class.</p>''',
                'website': 'https://workspace.google.com/education/',
                'features': [
                    ('Google Classroom', '<p>Centralise assignments and communication per class.</p>', '<p><strong>How to use:</strong></p><ol><li>Go to classroom.google.com.</li><li>Click the plus and choose Create class.</li><li>Share the class code with your students.</li><li>Post assignments via the Classwork tab.</li></ol>'),
                    ('Sheets Formulas', '<p>Automatic calculations for gradebooks.</p>', '<p><strong>How to use:</strong></p><ol><li>Click a cell.</li><li>Type =SUM(A1:A10) or =AVERAGE(A1:A10).</li><li>Press Enter.</li><li>Formulas update live as values change.</li></ol>'),
                    ('Real-time Collaboration', '<p>Several learners editing the same file simultaneously.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a Doc.</li><li>Click Share and add editors.</li><li>Watch cursors appear live.</li><li>Use comments to discuss changes.</li></ol>'),
                ],
            },
            {
                'name': 'OneNote',
                'developer': 'Microsoft',
                'category': 'Productivity',
                'description': '''<h3>What it is</h3>
<p>OneNote is a digital notebook that syncs across every device. It captures quick observations during a lesson and makes them available later on any other device.</p>
<h3>What it helps you achieve</h3>
<p>This is the informal companion to your formal gradebook. It is where you record the qualitative story behind a number, the observations you notice mid-lesson and would otherwise forget by the end of the day.</p>''',
                'website': 'https://www.onenote.com/',
                'features': [
                    ('Notebook per class', '<p>Organise planning, observations and resources.</p>', '<p><strong>How to use:</strong></p><ol><li>File, then New Notebook.</li><li>Create sections: Planning, Observations, Resources.</li><li>Add pages inside each section.</li></ol>'),
                    ('Tags', '<p>Mark items needing follow-up.</p>', '<p><strong>How to use:</strong></p><ol><li>Select a note.</li><li>On the Home tab, click Tags and choose To Do.</li><li>Use Find Tags to review all tagged items.</li></ol>'),
                    ('Cross-device sync', '<p>Capture on your phone, review on your laptop.</p>', '<p><strong>How to use:</strong></p><ol><li>Install OneNote on both devices.</li><li>Sign in with the same Microsoft account.</li><li>Notes sync automatically.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Working Gradebook and Lesson Slide Deck',
            'description': '''<h3>What this assignment is about</h3>
<p>Two artifacts, both drawn from your real teaching. The first is a working gradebook that saves you time and surfaces patterns you would otherwise miss. The second is a professionally designed lesson slide deck that looks like it was made by a designer, not improvised slide by slide.</p>
<h3>The three tools you will use</h3>
<h4>Excel (or Google Sheets)</h4>
<p>A spreadsheet with formulas and conditional formatting is a living gradebook. Instead of scanning rows for a struggling learner, you flag them automatically. Instead of retyping averages, you calculate them once. Instead of summarising a term by hand, you build a pivot table or chart that summarises the class for you.</p>
<h4>PowerPoint (or Google Slides)</h4>
<p>The slide deck is the teacher-facing output. The Slide Master is what separates a deck that looks professional from one that looks improvised. Once you set it, every slide inherits the same fonts, colours, and layout, without you touching individual slides.</p>
<h4>OneNote (or Google Keep)</h4>
<p>The digital notebook is where you record the qualitative observations that numbers cannot capture. It is your running record of who is engaged, who is struggling, who is quietly thriving, and it feeds back into your gradebook the moment a pattern emerges.</p>
<h3>The task</h3>
<ol>
<li>Build a gradebook for one of your classes in Excel or Google Sheets. Include at least eight learners and three assessments.</li>
<li>Add formulas that calculate row and column totals and averages.</li>
<li>Add conditional formatting that flags any learner below fifty percent.</li>
<li>Build one chart that visualises class trends.</li>
<li>Build a five-slide lesson using a single Slide Master theme, with one purposeful animation sequence.</li>
<li>Export the slide deck as a short video file and submit both links.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>Two clean, shareable artifacts. The gradebook should look like it would actually be used in a real staff room, not a spreadsheet exercise. The slide deck should look consistent, uncluttered, and clearly designed by someone who understands the Slide Master. If you have used OneNote to log observations behind the numbers, mention it in your submission note.</p>''',
            'prompt': '''<p>Submit two shareable links:</p>
<ol>
<li>A working gradebook (Excel, Google Sheets or similar) with at least eight learners, three assessments, formulas, conditional formatting and one chart.</li>
<li>A five-slide lesson deck built on a single Slide Master theme, exported as a video.</li>
</ol>
<p>In the submission notes, briefly explain what each artifact does and how you built it.</p>''',
            'submission_type': 'both',
            'rubric': [
                ('Gradebook functionality', '<p>Formulas and conditional formatting work correctly.</p>', 25),
                ('Gradebook clarity', '<p>Easy to read; a colleague could pick it up and use it.</p>', 25),
                ('Slide Master applied', '<p>The deck is consistent throughout and looks professional.</p>', 25),
                ('Purposeful animation', '<p>Animation sequences information, not decorates it.</p>', 25),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 5
    # ------------------------------------------------------------------
    {
        'number': 5,
        'title': 'Visual and Multimedia Content Creation',
        'week_description': '''<h3>What this week is about</h3>
<p>You will learn five tools that turn plain content into visually engaging learning materials. Canva for design, H5P for interactive content, Book Creator for learner-authored books, Edpuzzle for interactive video, and Loom for screen-recorded explainers.</p>
<p>You will finish the week with a complete multimedia lesson pack: one Canva resource and one Edpuzzle video lesson on the same topic.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Create differentiated, professionally branded teaching materials</li>
<li>Produce a short instructional video with embedded comprehension checks</li>
<li>Author interactive content from existing materials</li>
</ul>''',
        'topics': [],
        'tools': [
            {
                'name': 'Canva for Education',
                'developer': 'Canva Pty Ltd',
                'category': 'Visual and Multimedia',
                'description': '''<h3>What it is</h3>
<p>Canva is a drag-and-drop design tool with thousands of pre-made templates. It is built for people who have real design needs but no design training.</p>
<h3>What it helps you achieve</h3>
<p>Canva gives you professional-looking worksheets, posters, infographics and presentations without needing to learn graphic design. You start from a template, swap in your content, and the result is polished by default. Canva for Education is free for verified teachers.</p>''',
                'website': 'https://www.canva.com/education/',
                'features': [
                    ('Templates library', '<p>Start fast with pre-made professional designs.</p>', '<p><strong>How to use:</strong></p><ol><li>Log in to Canva.</li><li>Search for a template type such as worksheet or infographic.</li><li>Pick one that fits your content.</li><li>Edit text and images.</li></ol>'),
                    ('Brand Kit', '<p>Keep school colours and logos consistent.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the Brand Kit in the sidebar.</li><li>Upload your logo.</li><li>Add brand colours and fonts.</li><li>Apply across all your designs.</li></ol>'),
                    ('Classroom assignments', '<p>Assign design tasks directly to learners.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the Classroom tab.</li><li>Click Create assignment.</li><li>Choose a Canva template for students.</li><li>Share with the class.</li></ol>'),
                ],
            },
            {
                'name': 'H5P',
                'developer': 'Joubel',
                'category': 'Visual and Multimedia',
                'description': '''<h3>What it is</h3>
<p>H5P is a free, open-source authoring tool that inserts interactive checkpoints into existing content: questions inside a video, drag-and-drop tasks inside a diagram, branching scenarios inside a presentation.</p>
<h3>What it helps you achieve</h3>
<p>H5P turns passive content into active learning. A learner cannot skip past a video without answering the embedded question. It is the fastest way to convert one of your existing videos or diagrams into a self-checking activity.</p>''',
                'website': 'https://h5p.org/',
                'features': [
                    ('Interactive video', '<p>Embed questions at timestamps inside any video.</p>', '<p><strong>How to use:</strong></p><ol><li>Choose Interactive Video in the H5P editor.</li><li>Upload or paste a video URL.</li><li>Add interaction points at chosen timestamps.</li><li>Insert multiple-choice or open questions.</li></ol>'),
                    ('Course presentation', '<p>Build a slide deck with embedded quizzes.</p>', '<p><strong>How to use:</strong></p><ol><li>Choose Course Presentation.</li><li>Add slides with text, images, video.</li><li>Insert quiz slides between content slides.</li><li>Publish and embed in your LMS.</li></ol>'),
                    ('Drag the Words', '<p>Learners drag missing words into a sentence.</p>', '<p><strong>How to use:</strong></p><ol><li>Choose Drag the Words.</li><li>Enter text with asterisks marking the gaps.</li><li>Set options.</li><li>Publish.</li></ol>'),
                ],
            },
            {
                'name': 'Edpuzzle',
                'developer': 'Edpuzzle, Inc.',
                'category': 'Visual and Multimedia',
                'description': '''<h3>What it is</h3>
<p>Edpuzzle takes any video and lets you insert questions at specific timestamps, so a learner cannot skip ahead without answering.</p>
<h3>What it helps you achieve</h3>
<p>This is your flipped-classroom anchor. It converts a passive video into an active learning task with real data on who watched, who understood, and who did not. The completion report shows you exactly which question the class struggled with, before you even enter the classroom.</p>''',
                'website': 'https://edpuzzle.com/',
                'features': [
                    ('Video trimming', '<p>Cut a video to just the relevant section.</p>', '<p><strong>How to use:</strong></p><ol><li>Upload or search for a video.</li><li>Use the crop tool to trim start and end.</li><li>Preview the trimmed version.</li></ol>'),
                    ('Embedded questions', '<p>Insert questions at chosen timestamps.</p>', '<p><strong>How to use:</strong></p><ol><li>Click the question icon in the editor.</li><li>Choose multiple-choice or open-ended.</li><li>Write the question.</li><li>Drag it to the desired point in the timeline.</li></ol>'),
                    ('Completion reports', '<p>See which question the class struggled with.</p>', '<p><strong>How to use:</strong></p><ol><li>Assign to a class.</li><li>Open the Reports tab.</li><li>Filter by question or by learner.</li></ol>'),
                ],
            },
            {
                'name': 'Loom',
                'developer': 'Loom, Inc.',
                'category': 'Visual and Multimedia',
                'description': '''<h3>What it is</h3>
<p>Loom records your screen, your webcam, or both, and instantly produces a shareable video link. No editing software, no file exports.</p>
<h3>What it helps you achieve</h3>
<p>Two use cases. A worked-example walkthrough you record once and reuse every term. And individualized spoken feedback on one specific learner\'s work, which most teachers find lands harder emotionally than a written comment.</p>''',
                'website': 'https://www.loom.com/',
                'features': [
                    ('Screen and webcam recording', '<p>Record your screen and face at the same time.</p>', '<p><strong>How to use:</strong></p><ol><li>Install the Loom extension.</li><li>Click the Loom icon.</li><li>Choose screen plus camera.</li><li>Click Start Recording.</li></ol>'),
                    ('Instant share link', '<p>A shareable link is generated automatically.</p>', '<p><strong>How to use:</strong></p><ol><li>Stop recording.</li><li>The share link is copied to your clipboard.</li><li>Paste it anywhere.</li></ol>'),
                    ('Trim and chapters', '<p>Cut the start and end and add chapter markers.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a recording in Loom.</li><li>Click Trim.</li><li>Add chapter titles in the editor.</li></ol>'),
                ],
            },
            {
                'name': 'Book Creator',
                'developer': 'Red Jumper Studio',
                'category': 'Visual and Multimedia',
                'description': '''<h3>What it is</h3>
<p>Book Creator lets learners (not just teachers) build multimedia digital books that combine text, images and audio narration on each page.</p>
<h3>What it helps you achieve</h3>
<p>This is a learner-authoring tool. Use it for Language and Literacy digital storytelling, or for reflective portfolios that document a unit of work. The learner is the author, and the tool lowers the barrier to creating something genuinely presentable.</p>''',
                'website': 'https://bookcreator.com/',
                'features': [
                    ('Page templates', '<p>Comic, portrait or square layouts.</p>', '<p><strong>How to use:</strong></p><ol><li>Create a new book.</li><li>Choose a page template.</li><li>Add pages as you go.</li></ol>'),
                    ('Audio narration', '<p>Learners record their own voice per page.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a page.</li><li>Click the plus icon.</li><li>Choose Audio.</li><li>Record, then place the clip on the page.</li></ol>'),
                    ('Class library publishing', '<p>Share finished books with the class.</p>', '<p><strong>How to use:</strong></p><ol><li>Click the publish icon.</li><li>Choose Publish to Library.</li><li>Classmates can read and comment.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Multimedia Lesson Pack',
            'description': '''<h3>What this assignment is about</h3>
<p>You will build a complete multimedia pack for one topic: a design resource in Canva and an interactive video in Edpuzzle. The two artifacts serve the same learning goal, giving learners two different entry points into the same content.</p>
<h3>The two tools you will use</h3>
<h4>Canva for Education</h4>
<p>Canva removes the need for design training. You start from a template, swap in your content, and the result looks professional. For this assignment, use it to build the learner-facing resource: a worksheet, an infographic, or a poster that anchors the topic. Choose a template that matches the cognitive level of the task, not one that merely looks attractive.</p>
<h4>Edpuzzle</h4>
<p>Edpuzzle turns a passive video into an active learning task. Choose an existing video on your topic, embed at least four comprehension questions at meaningful pause points, and assign it. The completion report will tell you who watched, who understood, and which question needs re-teaching. That data becomes an asset to your next lesson.</p>
<h3>The task</h3>
<ol>
<li>Choose one topic you are currently teaching or will teach soon.</li>
<li>In Canva, build a one-page resource for that topic. Apply the Brand Kit if you have one, or set a consistent colour palette.</li>
<li>In Edpuzzle, find an existing video on the same topic. Embed at least four comprehension questions at meaningful pause points.</li>
<li>Write a short reflection: what does each artifact add, and how do they serve the same learning goal from different angles?</li>
<li>Submit both links plus the reflection.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>Two polished artifacts and a clear reflection. The Canva resource should look designed, not improvised. The Edpuzzle questions should check real comprehension, not just surface facts. The reflection should explain why you chose this combination for this topic, not just describe what you built.</p>''',
            'prompt': '''<p>Submit three items:</p>
<ol>
<li>A shareable link to your Canva resource (one page).</li>
<li>A shareable link to your Edpuzzle interactive video (with at least four embedded questions).</li>
<li>A short written reflection (300 to 500 words) explaining what each artifact adds and how they serve the same learning goal.</li>
</ol>''',
            'submission_type': 'both',
            'rubric': [
                ('Canva design quality', '<p>Professional, on-brand, readable.</p>', 25),
                ('Edpuzzle question quality', '<p>Questions check real comprehension, not surface recall.</p>', 25),
                ('Topic alignment', '<p>Both artifacts serve the same learning goal.</p>', 25),
                ('Reflection depth', '<p>Explains the pedagogical reasoning, not just the tools.</p>', 25),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 6
    # ------------------------------------------------------------------
    {
        'number': 6,
        'title': 'Interactive and Collaborative Classroom Tools',
        'week_description': '''<h3>What this week is about</h3>
<p>You will learn eight tools that turn one-way lessons into two-way participation. Nearpod and Pear Deck for interactive slides, Padlet and Miro for collaborative boards, and Kahoot!, Wayground, Socrative and Plickers for formative checks.</p>
<p>The aim of the week is not to use all eight. It is to know when to reach for which one, and to run one fully interactive lesson using at least three of them together.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Run a live, fully interactive lesson using real-time polling and collaboration</li>
<li>Facilitate asynchronous collaborative work between sessions</li>
<li>Choose the right tool for the device and connectivity context</li>
</ul>''',
        'topics': [],
        'tools': [
            {
                'name': 'Nearpod',
                'developer': 'Renaissance Learning',
                'category': 'Interactive and Collaborative',
                'description': '''<h3>What it is</h3>
<p>Nearpod converts an ordinary slide deck into an interactive one by inserting polls, open questions, drawing boards and quizzes between content slides. It runs in teacher-paced or student-paced mode.</p>
<h3>What it helps you achieve</h3>
<p>Nearpod keeps the whole class responding, not just watching. The teacher-paced mode suits direct instruction and whole-class discussion; student-paced mode suits independent or differentiated work. The post-session report shows you exactly who needs follow-up.</p>''',
                'website': 'https://nearpod.com/',
                'features': [
                    ('Interactive slides', '<p>Insert polls, open questions and drawing boards.</p>', '<p><strong>How to use:</strong></p><ol><li>Upload an existing deck or build new.</li><li>Add Slide, then Interactive.</li><li>Choose Poll, Open-Ended, Draw It or Quiz.</li></ol>'),
                    ('Teacher-paced versus student-paced', '<p>Live-together or independent work.</p>', '<p><strong>How to use:</strong></p><ol><li>After building, click Live Participation for whole-class.</li><li>Choose Student-Paced for independent work.</li></ol>'),
                    ('Post-session reports', '<p>See which learners need follow-up.</p>', '<p><strong>How to use:</strong></p><ol><li>After the session, open Reports.</li><li>Sort by learner or by question.</li><li>Note low performers for re-teaching.</li></ol>'),
                ],
            },
            {
                'name': 'Padlet',
                'developer': 'Padlet',
                'category': 'Interactive and Collaborative',
                'description': '''<h3>What it is</h3>
<p>Padlet is a shared digital board, a kind of online corkboard, where everyone in the room can pin a note at the same time from their own device. It comes in several layouts: Wall, Grid, Shelf, Map, Timeline.</p>
<h3>What it helps you achieve</h3>
<p>Its fastest win is an anonymous exit ticket: instant, honest feedback with no preparation. Once that is comfortable, try the Map or Timeline layout for Geography or History. QR-code sharing makes it usable even in classrooms with only a few shared devices.</p>''',
                'website': 'https://padlet.com/',
                'features': [
                    ('Multiple layouts', '<p>Wall, Grid, Shelf, Map or Timeline.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Make a Padlet.</li><li>Choose a layout.</li><li>Set your title and description.</li></ol>'),
                    ('Posting permissions', '<p>Anonymous or named, editable or view-only.</p>', '<p><strong>How to use:</strong></p><ol><li>Open settings, then Privacy.</li><li>Choose who can post.</li><li>Optionally allow anonymous posts.</li></ol>'),
                    ('QR-code sharing', '<p>Share instantly in low-device classrooms.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Share.</li><li>Click the QR icon.</li><li>Project it, learners scan and post.</li></ol>'),
                ],
            },
            {
                'name': 'Kahoot!',
                'developer': 'Kahoot! ASA',
                'category': 'Interactive and Collaborative',
                'description': '''<h3>What it is</h3>
<p>Kahoot! is the most well-known gamified quiz tool in education. Questions appear on a shared screen; learners answer on their own device; a leaderboard rewards speed and accuracy together.</p>
<h3>What it helps you achieve</h3>
<p>Kahoot! is excellent for rapid recall review before a test. It is less suited to teaching brand-new content for the first time, and it is worth being honest with yourself about that distinction.</p>''',
                'website': 'https://kahoot.com/',
                'features': [
                    ('Quiz builder', '<p>Create or adapt multiple-choice quizzes.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Create.</li><li>Add questions and answers.</li><li>Set timing and points.</li></ol>'),
                    ('Live hosting', '<p>Project the quiz and share the game PIN.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Play.</li><li>Choose Classic or Team Mode.</li><li>Share the PIN with the class.</li></ol>'),
                    ('Per-question reports', '<p>See which question the class struggled with.</p>', '<p><strong>How to use:</strong></p><ol><li>After the session, open Reports.</li><li>Click each question to see accuracy.</li></ol>'),
                ],
            },
            {
                'name': 'Plickers',
                'developer': 'Plickers, Inc.',
                'category': 'Interactive and Collaborative',
                'description': '''<h3>What it is</h3>
<p>Plickers solves a specific problem: formative assessment in a classroom where only the teacher has an internet-capable device. Every learner holds up a printed card, rotated to show their answer, and the teacher\'s phone camera scans the whole room.</p>
<h3>What it helps you achieve</h3>
<p>This is proof that meaningful EdTech does not require one device per learner. Worth remembering any time budget or access feels like a barrier to using technology at all.</p>''',
                'website': 'https://plickers.com/',
                'features': [
                    ('Printed cards', '<p>Free printable PDF for the whole class.</p>', '<p><strong>How to use:</strong></p><ol><li>Log in to Plickers.com.</li><li>Go to Classes, then Print Cards.</li><li>Print one card per learner.</li></ol>'),
                    ('Question sets', '<p>Create multiple-choice questions in the app.</p>', '<p><strong>How to use:</strong></p><ol><li>Go to Library, then New Question.</li><li>Enter text and four answer choices.</li><li>Assign to a class.</li></ol>'),
                    ('Phone scan', '<p>Capture the whole class\'s answers instantly.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the Plickers app on your phone.</li><li>Select a question.</li><li>Scan the room with the camera.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Fully Interactive Lesson Delivery',
            'description': '''<h3>What this assignment is about</h3>
<p>You will design and deliver (or record) one lesson using at least three tools from this week. The goal is not to use as many tools as possible, but to use the right three for the pedagogical moments of your lesson: the opener, the collaborative middle, and the formative check at the end.</p>
<h3>The tools you will draw from</h3>
<h4>Nearpod</h4>
<p>Converts a slide deck into an interactive one. Use it to keep the whole class responding throughout a lesson rather than watching passively. Teacher-paced mode suits direct instruction; student-paced mode suits independent work.</p>
<h4>Padlet</h4>
<p>A shared digital board. Use it for an anonymous exit ticket, a group brainstorm, or a collaborative note board. The QR-code sharing feature makes it work even with a few shared devices.</p>
<h4>Kahoot!</h4>
<p>Live gamified quiz for rapid recall review. Use it for the formative check at the end of a lesson, or to launch a lesson with a competitive warm-up.</p>
<h4>Plickers</h4>
<p>Low-device formative assessment with printed cards. Use it when student devices are limited or when you want to check the whole class quickly and visibly.</p>
<h3>The task</h3>
<ol>
<li>Choose a lesson you already plan to teach.</li>
<li>Choose three tools from this week that fit three distinct moments of the lesson: an interactive opener or a collaborative activity or a formative check.</li>
<li>Design the lesson around those three moments. Be specific about which tool serves which moment.</li>
<li>Either deliver the lesson live with your class, or record a screen-capture walkthrough of the lesson as you would run it.</li>
<li>Write a short reflection on what each tool contributed and what you would change next time.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A recorded lesson or a detailed lesson plan with a recording of the tool sequences. The three tools should serve three genuinely different purposes, not just decorate the lesson. The reflection should be honest about what worked and what did not.</p>''',
            'prompt': '''<p>Submit two items:</p>
<ol>
<li>A link to your recorded lesson (or a detailed lesson plan plus a screen recording of the tool sequences).</li>
<li>A short reflection (300 to 500 words) on what each tool contributed and what you would change next time.</li>
</ol>
<p>Ensure the lesson uses at least three tools from this week, each serving a distinct pedagogical moment.</p>''',
            'submission_type': 'both',
            'rubric': [
                ('Tool variety', '<p>Three different tools used purposefully.</p>', 25),
                ('Pedagogical fit', '<p>Each tool fits the pedagogical moment it is used in.</p>', 25),
                ('Learner engagement', '<p>Evidence of genuine learner participation.</p>', 25),
                ('Reflection depth', '<p>Specific and honest, not generic.</p>', 25),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 7
    # ------------------------------------------------------------------
    {
        'number': 7,
        'title': 'Gamification and Game-Based Learning',
        'week_description': '''<h3>What this week is about</h3>
<p>You will learn the difference between gamification (adding game mechanics like points, badges and leaderboards to existing content) and game-based learning (using a full game as the primary vehicle for the content). Both are covered, and both are treated seriously.</p>
<p>The governing principle of the week: a mechanic is only worth using if it reinforces a specific, stated learning objective. Engagement without a tied objective is decoration, not pedagogy. The failure mode is sometimes called chocolate-covered broccoli.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Distinguish gamification from game-based learning</li>
<li>Design a gamified sequence that serves an objective, not just novelty</li>
<li>Select gamification tools appropriate to a subject</li>
</ul>''',
        'topics': [
            {
                'title': 'The governing principle: mechanics must serve objectives',
                'description': '<p>A mechanic is only worth using if it reinforces a specific, stated learning objective. Engagement without a tied objective is decoration, not pedagogy. Every tool in this week runs through that filter.</p>',
                'materials': [{'title': 'The chocolate-covered broccoli failure mode', 'content': '<p>When the game looks fun but the learning is thin or absent. The defence is to pair every session with a content-level accuracy check, not just an enjoyment check.</p>', 'url': ''}],
            },
        ],
        'tools': [
            {
                'name': 'Gimkit',
                'developer': 'Gimkit, Inc.',
                'category': 'Gamification',
                'description': '''<h3>What it is</h3>
<p>Gimkit layers a game-show style in-game economy onto quiz review. Learners earn virtual currency for correct answers and spend it on power-ups, which sustains engagement over a longer review session than a single quiz round.</p>
<h3>What it helps you achieve</h3>
<p>Gimkit keeps a longer revision block interesting. Its Team Mode in particular adds a collaborative spending decision layer that genuinely distinguishes it from Kahoot or Wayground. Pair every session with an accuracy check afterward so you can see the fun did not come at the expense of learning.</p>''',
                'website': 'https://www.gimkit.com/',
                'features': [
                    ('Kits', '<p>Build or import question sets.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Create.</li><li>Add questions or import from a quiz file.</li><li>Save the set as a kit.</li></ol>'),
                    ('Team Mode', '<p>Collaborative spending decisions add strategy.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Play.</li><li>Choose Team Mode.</li><li>Assign learners to teams.</li></ol>'),
                    ('In-game economy', '<p>Learners spend earned currency on power-ups.</p>', '<p><strong>How to use:</strong></p><ol><li>Learners earn cash per correct answer.</li><li>They open the shop mid-game.</li><li>They purchase power-ups strategically.</li></ol>'),
                ],
            },
            {
                'name': 'Quizlet',
                'developer': 'Quizlet, Inc.',
                'category': 'Gamification',
                'description': '''<h3>What it is</h3>
<p>Quizlet is a flashcard platform built around a simple term-definition pair, with game modes such as Match (timed pairing) and Gravity (fast typing) layered on top.</p>
<h3>What it helps you achieve</h3>
<p>Quizlet is your go-to whenever a subject has a heavy vocabulary load: Languages, Biology, History terminology. It is less essential for subjects that are mostly about reasoning rather than recall. Quizlet Live, the real-time team mode, is the single feature that turns solitary flashcard review into a shared classroom event.</p>''',
                'website': 'https://quizlet.com/',
                'features': [
                    ('Study sets', '<p>Create term and definition pairs.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Create.</li><li>Enter terms and definitions.</li><li>Save the set.</li></ol>'),
                    ('Match game', '<p>Timed pairing of terms and definitions.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a set.</li><li>Choose Match.</li><li>Race to clear the board.</li></ol>'),
                    ('Quizlet Live', '<p>Real-time team-based review.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a set.</li><li>Click Live.</li><li>Share the join code with the class.</li></ol>'),
                ],
            },
            {
                'name': 'CodeCombat',
                'developer': 'CodeCombat, Inc.',
                'category': 'Gamification',
                'description': '''<h3>What it is</h3>
<p>CodeCombat teaches real Python or JavaScript through a game where learners write actual code to move a character through puzzle levels. Not drag-and-drop blocks, real code from early on.</p>
<h3>What it helps you achieve</h3>
<p>CodeCombat belongs specifically in Computer Science contexts (IGCSE and IB Computer Science, and the CBE digital-literacy strand). The teacher dashboard shows exactly which line of code each learner is stuck on, which is a genuine diagnostic help for teachers with limited coding background themselves.</p>''',
                'website': 'https://codecombat.com/',
                'features': [
                    ('Course levels', '<p>Assign based on prior experience.</p>', '<p><strong>How to use:</strong></p><ol><li>Create a class.</li><li>Assign learners to a course level.</li><li>Track progress by level.</li></ol>'),
                    ('Real code entry', '<p>Learners write genuine Python or JavaScript.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a level.</li><li>Type code in the editor.</li><li>Click Run.</li></ol>'),
                    ('Teacher dashboard', '<p>See exactly which line each learner is stuck on.</p>', '<p><strong>How to use:</strong></p><ol><li>Open your class dashboard.</li><li>Click a learner.</li><li>View the specific line of code they last ran.</li></ol>'),
                ],
            },
            {
                'name': 'Quizlet and Brainscape', 
                'developer': 'Quizlet / Brainscape LLC',
                'category': 'Gamification',
                'description': '''<h3>What it is</h3>
<p>Quizlet uses flashcards with game modes. Brainscape uses spaced repetition: learners self-rate their confidence on each card, and the algorithm resurfaces low-confidence cards more often.</p>
<h3>What it helps you achieve</h3>
<p>Quizlet is quick, game-adjacent review for vocabulary-heavy subjects. Brainscape builds durable long-term retention, and its one rule is that review must be spread across days, not crammed in one session. Use Quizlet for in-class review and Brainscape for spaced homework.</p>''',
                'website': 'https://www.brainscape.com/',
                'features': [
                    ('Deck builder', '<p>Create flashcards for high-recall content.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Create.</li><li>Add cards.</li><li>Assign to your class.</li></ol>'),
                    ('Confidence rating', '<p>Learners self-rate 1 to 5 per card.</p>', '<p><strong>How to use:</strong></p><ol><li>Review a card.</li><li>Rate your confidence.</li><li>The algorithm resurfaces low-confidence cards.</li></ol>'),
                    ('Class reports', '<p>See persistent low-confidence items.</p>', '<p><strong>How to use:</strong></p><ol><li>Open Reports.</li><li>Sort by confidence.</li><li>Plan re-teaching.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Gamified Mini-Unit with Justification Memo',
            'description': '''<h3>What this assignment is about</h3>
<p>You will design a two-lesson gamified sequence for a topic you teach, using at least two tools from this week. Then you will write a justification memo that explains, mechanic by mechanic, why each choice serves a specific learning objective. The memo is the more important half of the assignment.</p>
<h3>The tools you will draw from</h3>
<h4>Gimkit</h4>
<p>Game-show style quiz with an in-game economy. Use it for a longer revision block where you want sustained engagement. Its Team Mode adds collaborative spending decisions that distinguish it from a simple quiz.</p>
<h4>Quizlet</h4>
<p>Flashcard platform with Match and Gravity game modes. Best for vocabulary-heavy topics. Quizlet Live turns solitary review into a shared classroom event.</p>
<h4>CodeCombat</h4>
<p>Game-based coding instruction in real Python or JavaScript. Best for Computer Science contexts. The teacher dashboard shows exactly which line of code each learner is stuck on.</p>
<h4>Brainscape</h4>
<p>Spaced-repetition flashcards. Best for memory-heavy subjects. Its one rule: review must be spread across days, not crammed.</p>
<h3>The task</h3>
<ol>
<li>Choose a topic you currently teach or are about to teach.</li>
<li>Design a two-lesson gamified mini-unit. Each lesson should use at least one tool from this week.</li>
<li>Write a memo of at least four hundred words. For each mechanic you chose, name the specific learning objective it serves. Be explicit: does this mechanic reinforce the objective, or is it decoration?</li>
<li>Explain how you will verify content-level learning afterward, not just engagement.</li>
<li>Submit the memo and any materials you designed.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A coherent two-lesson sequence, not a grab-bag of tools. The memo is the centrepiece: it should read like a genuine argument for the choices you made, and it should be honest about the risks of gamification, including the chocolate-covered broccoli failure mode.</p>''',
            'prompt': '''<p>Submit two items:</p>
<ol>
<li>Your gamified mini-unit design (a lesson plan document or a recording of the two lessons).</li>
<li>A written memo (at least four hundred words) justifying each mechanic against a specific learning objective, and explaining how you will verify content-level learning afterward.</li>
</ol>''',
            'submission_type': 'both',
            'rubric': [
                ('Mechanics-to-objective fit', '<p>Each mechanic clearly serves a stated objective.</p>', 30),
                ('Tool choice', '<p>Tools chosen for pedagogical fit, not novelty.</p>', 20),
                ('Reflection quality', '<p>Acknowledges risks and demonstrates judgement.</p>', 25),
                ('Lesson coherence', '<p>A genuine two-lesson sequence, not a collection.</p>', 25),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 8
    # ------------------------------------------------------------------
    {
        'number': 8,
        'title': 'Assessment Technology and Learning Analytics',
        'week_description': '''<h3>What this week is about</h3>
<p>You will learn to use digital formative assessment tools to adjust your teaching in real time, and to read the analytics your LMS is already collecting. The two halves fit together: forms give you quick data, dashboards help you interpret a term of data.</p>
<p>You will also learn to build a digital rubric that is genuinely usable, with observable, specific criteria rather than vague descriptors.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Use digital formative assessment tools to adjust instruction</li>
<li>Read and act on an LMS or tool analytics dashboard</li>
<li>Build a digital rubric that learners can aim at</li>
</ul>''',
        'topics': [
            {
                'title': 'Digital Rubrics',
                'description': '<p>A scoring guide with named criteria and described performance levels. Share it with learners before the task, not just at grading time, and use observable language.</p>',
                'materials': [{'title': 'The rule about observable language', 'content': '<p>Good is not a rubric criterion. Includes three supporting details from the text is. Specific, observable language is the actual skill this week teaches.</p>', 'url': ''}],
            },
        ],
        'tools': [
            {
                'name': 'Google Forms',
                'developer': 'Google',
                'category': 'Assessment',
                'description': '''<h3>What it is</h3>
<p>Google Forms is an auto-graded quiz and survey builder. It grades submissions instantly when a correct-answer key is set.</p>
<h3>What it helps you achieve</h3>
<p>Forms turns a quick check into data you can act on. The automatic response summary shows which question the class struggled with, without you tallying anything by hand. This is the fastest feedback loop in the whole certificate.</p>''',
                'website': 'https://forms.google.com/',
                'features': [
                    ('Quiz mode', '<p>Turn any form into an auto-graded quiz.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a form.</li><li>Click Settings.</li><li>Enable Make this a quiz.</li><li>Add an answer key to each question.</li></ol>'),
                    ('Instant feedback', '<p>Release grades immediately or after manual review.</p>', '<p><strong>How to use:</strong></p><ol><li>In Settings, under Quizzes, choose Release grade immediately or Later, after manual review.</li></ol>'),
                    ('Response summary', '<p>See per-question accuracy automatically.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the Responses tab.</li><li>Click Summary.</li><li>Scroll through per-question breakdowns.</li></ol>'),
                ],
            },
            {
                'name': 'Microsoft Forms',
                'developer': 'Microsoft Corporation',
                'category': 'Assessment',
                'description': '''<h3>What it is</h3>
<p>Microsoft Forms is the Microsoft 365 equivalent to Google Forms. It provides auto-graded quizzes, shareable via link or Teams, with results exported to Excel.</p>
<h3>What it helps you achieve</h3>
<p>If your school already uses Microsoft Office and Teams, this is the natural choice. Results export straight into the gradebook workflow you built in Week 4, without re-typing anything.</p>''',
                'website': 'https://www.microsoft.com/en-us/microsoft-365/online-surveys',
                'features': [
                    ('Quiz builder', '<p>Create auto-graded quizzes.</p>', '<p><strong>How to use:</strong></p><ol><li>Click New Quiz.</li><li>Add questions with correct answers.</li><li>Assign points per question.</li></ol>'),
                    ('Teams embed', '<p>Embed the quiz directly into a class channel.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the quiz.</li><li>Click Share, then Embed in Teams.</li></ol>'),
                    ('Excel export', '<p>Export results for analysis.</p>', '<p><strong>How to use:</strong></p><ol><li>Open Responses.</li><li>Click Open in Excel.</li><li>Analyse in your gradebook.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Data-Informed Re-teach Plan',
            'description': '''<h3>What this assignment is about</h3>
<p>You will build a ten-question auto-graded quiz, run it with your class or with a simulated dataset, and then write a re-teach plan grounded specifically in what the data shows. This is the assignment that turns a quiz from a score machine into an instructional decision tool.</p>
<h3>The two tools you will use</h3>
<h4>Google Forms (or Microsoft Forms)</h4>
<p>Both auto-grade quizzes and both provide per-question accuracy summaries. Use whichever matches your school ecosystem. The important feature is the automatic summary: it tells you which question the class struggled with, without you tallying anything by hand.</p>
<h4>Excel or Google Sheets</h4>
<p>If you want to go further, export the responses to a spreadsheet and apply the pivot-table and chart skills from Week 4. But the minimum viable version is simply the automatic response summary inside Forms itself.</p>
<h3>The task</h3>
<ol>
<li>Build a ten-question quiz on a topic you have taught this term. Multiple-choice questions are easiest to auto-grade.</li>
<li>Run the quiz with your class, or simulate twenty learner responses if you prefer not to disrupt your class.</li>
<li>Open the per-question response summary.</li>
<li>Identify the single biggest skill gap the data reveals.</li>
<li>Write a one-paragraph re-teach plan: what specifically will you re-teach, with what activity, and how will you check whether the re-teach worked?</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A working quiz, a shareable link to the summary data, and a re-teach plan that names a specific skill gap rather than a general weakness. The plan should be actionable tomorrow morning, not a theoretical reflection.</p>''',
            'prompt': '''<p>Submit three items:</p>
<ol>
<li>A shareable link to your auto-graded quiz.</li>
<li>A shareable link to the response summary data (either real, or clearly labelled as simulated).</li>
<li>A one-paragraph re-teach plan naming the specific skill gap and how you will address it.</li>
</ol>''',
            'submission_type': 'both',
            'rubric': [
                ('Quiz construction', '<p>Ten clear, well-designed questions.</p>', 20),
                ('Data interpretation', '<p>Correctly reads per-question data.</p>', 30),
                ('Re-teach specificity', '<p>Names the exact skill gap and approach.</p>', 30),
                ('Actionability', '<p>Plan is realistic and specific.</p>', 20),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 9
    # ------------------------------------------------------------------
    {
        'number': 9,
        'title': 'Inclusive Design, Assistive Technology and Digital Citizenship',
        'week_description': '''<h3>What this week is about</h3>
<p>You will learn how to remove the specific barriers that stop some learners accessing your lessons, using tools already built into the devices and software you already have. You will also teach digital citizenship, online safety and academic integrity explicitly, rather than assuming learners absorb it by osmosis.</p>
<p>The week closes with an accessibility audit and redesign of one of your existing lesson resources.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Apply UDL using specific assistive technology</li>
<li>Remove at least one specific barrier in a lesson resource</li>
<li>Teach digital citizenship and academic integrity explicitly</li>
</ul>''',
        'topics': [
            {
                'title': 'Digital Citizenship Curriculum',
                'description': '<p>Ready-made lessons on online safety, digital footprint and cyberbullying, from Common Sense Education. The skill is localization: swap in examples your own learners recognize.</p>',
                'materials': [{'title': 'Common Sense Education, Digital Citizenship', 'content': '<p>Free lesson library covering privacy, cyberbullying, digital footprint, media balance and academic integrity.</p>', 'url': 'https://www.commonsense.org/education/digital-citizenship'}],
            },
        ],
        'tools': [
            {
                'name': 'Microsoft Immersive Reader',
                'developer': 'Microsoft Corporation',
                'category': 'Accessibility',
                'description': '''<h3>What it is</h3>
<p>Immersive Reader is a built-in text-to-speech and reading-support tool inside Word, OneNote, Teams and the Edge browser. It can read any document aloud, adjust spacing, and define unfamiliar words with a picture.</p>
<h3>What it helps you achieve</h3>
<p>Immersive Reader removes a specific decoding barrier so a learner can access content at the intended cognitive level. It is free, already on your devices, and helps struggling readers, English-language learners and any learner who benefits from hearing text as well as seeing it.</p>''',
                'website': 'https://www.microsoft.com/en-us/education/products/immersive-reader',
                'features': [
                    ('Read Aloud', '<p>Text-to-speech for any document.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a Word document or an Edge-rendered page.</li><li>Click the Immersive Reader icon.</li><li>Click Read Aloud.</li></ol>'),
                    ('Text spacing and font', '<p>Adjust readability for learners with dyslexia.</p>', '<p><strong>How to use:</strong></p><ol><li>In Immersive Reader, open Text Preferences.</li><li>Adjust spacing, font and background colour.</li></ol>'),
                    ('Picture Dictionary', '<p>Define unfamiliar words with a picture.</p>', '<p><strong>How to use:</strong></p><ol><li>Click any word.</li><li>Choose Picture Dictionary from the popup.</li><li>A picture and definition appear.</li></ol>'),
                ],
            },
            {
                'name': 'Read and Write (Texthelp)',
                'developer': 'Texthelp',
                'category': 'Accessibility',
                'description': '''<h3>What it is</h3>
<p>Read and Write is a literacy support toolbar with text-to-speech, dictionary, translation and word prediction. It is a browser extension on Chrome, and a standalone app on Windows, Mac and iPad.</p>
<h3>What it helps you achieve</h3>
<p>Where Immersive Reader focuses on reading access, Read and Write also supports written expression through word prediction and translation. Especially valuable in classrooms with English-language learners and diagnosed or undiagnosed reading and writing difficulties.</p>''',
                'website': 'https://www.texthelp.com/products/read-write-education/',
                'features': [
                    ('Read Aloud', '<p>Text-to-speech on any webpage or document.</p>', '<p><strong>How to use:</strong></p><ol><li>Install the Read and Write extension.</li><li>Highlight text.</li><li>Click the Read Aloud button.</li></ol>'),
                    ('Word Prediction', '<p>Suggests words as learners type.</p>', '<p><strong>How to use:</strong></p><ol><li>Open Word Prediction.</li><li>Begin typing.</li><li>Click a prediction to insert it.</li></ol>'),
                    ('Translation', '<p>Support multilingual learners accessing English content.</p>', '<p><strong>How to use:</strong></p><ol><li>Highlight text.</li><li>Click Translation.</li><li>Choose the target language.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Accessibility Audit and Redesign',
            'description': '''<h3>What this assignment is about</h3>
<p>You will take one reading-heavy resource you already use, audit it for the specific learners it silently excludes, and redesign it using at least two assistive technology tools. This is the assignment that moves UDL from theory to practice.</p>
<h3>The two tools you will use</h3>
<h4>Microsoft Immersive Reader</h4>
<p>A built-in reading support tool inside Word, OneNote, Teams and Edge. It reads text aloud, adjusts spacing, and defines words with pictures. Use it in your redesign to give a learner who struggles with decoding a way to access the same content at the same cognitive level as their peers.</p>
<h4>Read and Write (Texthelp)</h4>
<p>A literacy support toolbar that adds word prediction and translation on top of text-to-speech. Use it in your redesign for learners who struggle with writing or who are accessing content in a second language. Word prediction, in particular, removes the mechanical barrier that keeps a bright learner\'s ideas from reaching the page.</p>
<h3>The task</h3>
<ol>
<li>Choose one reading-heavy resource you currently use with your class.</li>
<li>Audit it: which learners would struggle, and specifically why? Name one to three distinct barriers.</li>
<li>Redesign the resource using at least two assistive tools. The redesign should genuinely remove the barriers you identified, not merely add tools on top.</li>
<li>Write a written audit (at least three hundred words) covering the barriers identified, the tools used, and the expected impact on specific learner profiles.</li>
<li>Submit both the original and the redesigned version, plus the audit.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A specific, learner-focused audit rather than a generic reflection on inclusion. The redesigned resource should look like something you would actually use in a real classroom. The audit should name specific learner profiles, not categories.</p>''',
            'prompt': '''<p>Submit three items:</p>
<ol>
<li>A link to the original resource.</li>
<li>A link to your redesigned resource using at least two assistive tools.</li>
<li>A written audit (at least three hundred words) covering barriers, tools and expected impact.</li>
</ol>''',
            'submission_type': 'both',
            'rubric': [
                ('Barrier identification', '<p>Specific and learner-focused, not generic.</p>', 25),
                ('Tool application', '<p>Two appropriate assistive tools applied well.</p>', 30),
                ('Redesign quality', '<p>The redesign genuinely removes barriers.</p>', 25),
                ('Written reflection', '<p>Names specific learner profiles and impacts.</p>', 20),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 10
    # ------------------------------------------------------------------
    {
        'number': 10,
        'title': 'AI Foundations, Ethics and Data Privacy in Education',
        'week_description': '''<h3>What this week is about</h3>
<p>This week is deliberately reference-based rather than tool-based. It is a pause before hands-on AI use in Week 11, matching the principle that trust and safety must be established before capability. You will learn how generative AI actually works, why it confidently produces wrong output sometimes, and what is and is not safe to enter into a tool when a real learner\'s data is involved.</p>
<p>You will finish the week with a written AI-use policy you could bring directly to your own school or classroom.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Explain how generative AI works, well enough to teach it responsibly</li>
<li>Apply a data-privacy checklist before using any AI tool with students</li>
<li>Write a school-ready AI-use policy grounded in the Kenya Data Protection Act</li>
</ul>''',
        'topics': [
            {
                'title': 'Generative AI Fundamentals',
                'description': '<p>Generative AI tools predict plausible text, image or audio output based on patterns in training data. They do not look up facts the way a search engine does. Hallucination is confident fabricated output presented as fact, a structural feature, not an occasional bug.</p>',
                'materials': [{'title': 'Prompt Engineering Overview, Anthropic', 'content': '<p>A practical overview of how prompting works and where models are reliable versus where they are not.</p>', 'url': 'https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview'}],
            },
            {
                'title': 'Kenya Data Protection Act 2019',
                'description': '<p>Enforced by the Office of the Data Protection Commissioner. Applies to any organisation processing personal data of people in Kenya, including schools. Children\'s data requires heightened protection.</p>',
                'materials': [{'title': 'Office of the Data Protection Commissioner, Kenya', 'content': '<p>The regulator\'s official site, including guidance on children\'s data and school obligations.</p>', 'url': 'https://www.odpc.go.ke/'}],
            },
        ],
        'tools': [],
        'assignment': {
            'title': 'Classroom AI-Use Policy',
            'description': '''<h3>What this assignment is about</h3>
<p>You will write a one-page AI-use policy that a school director or head of department could adopt with minimal editing. The policy must be grounded in the Kenya Data Protection Act 2019 and must cover four specific areas: what tools are permitted, what data may never be entered, how academic integrity will be checked, and what teachers must review before AI output reaches a learner.</p>
<h3>The two frameworks you will use</h3>
<h4>Generative AI fundamentals</h4>
<p>AI tools predict plausible output rather than retrieving facts. This is the reason every policy must include a review step: no AI output should reach a learner without teacher verification. Hallucination is not an occasional bug, it is a structural feature, and the policy must reflect that.</p>
<h4>The Kenya Data Protection Act 2019</h4>
<p>The Act applies to any organisation processing personal data of people in Kenya, including schools. Children\'s data, including academic records, requires heightened protection. Most free-tier consumer AI tools may use submitted data to further train their models unless an education-specific agreement states otherwise. Your policy must state, explicitly, what data may not be entered, and what approval process a school must follow before adopting a tool.</p>
<h3>The task</h3>
<ol>
<li>Write a one-page policy for your own classroom or school.</li>
<li>Reference the Kenya Data Protection Act 2019 explicitly, including the ODPC as the enforcement body.</li>
<li>Cover the four required areas: permitted tools, prohibited data, academic integrity verification, teacher review requirements.</li>
<li>Include a short section on how the policy will be reviewed annually or when the tool landscape changes significantly.</li>
<li>Submit a link to the policy document.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A policy that a director would sign without significant rewriting. It should be clear, specific and enforceable. Avoid vague language like should be careful with data. Specify what categories of data are prohibited, what approval process exists, and what verification step is required before AI output reaches a learner.</p>''',
            'prompt': '''<p>Submit a link to a one-page AI-use policy covering:</p>
<ul>
<li>The legal foundation, with explicit reference to the Data Protection Act 2019 and the ODPC</li>
<li>Permitted tools and prohibited data categories</li>
<li>Academic integrity verification</li>
<li>Teacher review requirements before AI output reaches a learner</li>
<li>A review and revision process</li>
</ul>''',
            'submission_type': 'link',
            'rubric': [
                ('Legal grounding', '<p>Correctly references the DPA and the ODPC.</p>', 25),
                ('Data handling rules', '<p>Clear and specific about prohibited data.</p>', 25),
                ('Academic integrity', '<p>Concrete approach, not just a warning.</p>', 25),
                ('Usability', '<p>A school director could adopt this policy with minimal editing.</p>', 25),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 11
    # ------------------------------------------------------------------
    {
        'number': 11,
        'title': 'AI Tools in Practice',
        'week_description': '''<h3>What this week is about</h3>
<p>Now that you understand how AI works and what data is safe to enter, you will use a stack of AI tools to reduce planning and grading time while retaining your own oversight. Every tool in this week follows the same rule: whatever it produces is a first draft, not a finished product, until you have reviewed and corrected it.</p>
<p>You will finish the week with a complete AI-assisted lesson pack that documents every correction you made.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Use a stack of AI tools to reduce planning and grading time</li>
<li>Apply the Week 10 privacy checklist to real tool choices</li>
<li>Document the corrections you made so the pack is genuinely yours</li>
</ul>''',
        'topics': [],
        'tools': [
            {
                'name': 'MagicSchool AI',
                'developer': 'MagicSchool AI, Inc.',
                'category': 'AI Tools',
                'description': '''<h3>What it is</h3>
<p>MagicSchool is a broad-purpose planning assistant with over eighty purpose-built generators: lesson plans, rubrics, parent letters, IEP accommodations, and more.</p>
<h3>What it helps you achieve</h3>
<p>MagicSchool reduces the blank-page problem. It gives you a strong first draft in minutes, which you then revise against your own goals. The output is only as good as the context you provide, so specific inputs (grade, topic, standard) matter far more than vague prompts.</p>''',
                'website': 'https://www.magicschool.ai/',
                'features': [
                    ('Lesson Plan Generator', '<p>First-draft planning.</p>', '<p><strong>How to use:</strong></p><ol><li>Select the Lesson Plan tool.</li><li>Enter grade, topic, curriculum standard.</li><li>Generate, then edit against your goals.</li></ol>'),
                    ('Rubric Generator', '<p>Draft a starting rubric.</p>', '<p><strong>How to use:</strong></p><ol><li>Choose Rubric Generator.</li><li>Enter your criteria.</li><li>Adjust descriptors to your school\'s language.</li></ol>'),
                    ('IEP Accommodation writer', '<p>Suggest accommodations from an input profile.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the IEP Accommodation tool.</li><li>Describe the learner profile, anonymized.</li><li>Review and adapt suggestions.</li></ol>'),
                ],
            },
            {
                'name': 'Diffit',
                'developer': 'Diffit',
                'category': 'AI Tools',
                'description': '''<h3>What it is</h3>
<p>Diffit takes any text, a passage, a URL or a topic, and generates several versions at different reading levels automatically, along with vocabulary support and comprehension questions.</p>
<h3>What it helps you achieve</h3>
<p>Diffit is the single fastest tool to win over a mixed-ability classroom. It solves the problem every teacher has felt: one reading passage, one reading level, and a class with three levels in it.</p>''',
                'website': 'https://web.diffit.me/',
                'features': [
                    ('Multi-level texts', '<p>Same content at three or four reading levels.</p>', '<p><strong>How to use:</strong></p><ol><li>Paste a passage or topic.</li><li>Click Generate.</li><li>Choose levels for your class range.</li></ol>'),
                    ('Vocabulary support', '<p>Auto-generated vocabulary lists.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the Vocabulary panel.</li><li>Review definitions for subject accuracy before sharing.</li></ol>'),
                    ('Comprehension questions', '<p>Auto-generated checks per level.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Questions.</li><li>Select multiple-choice or short answer.</li><li>Edit as needed.</li></ol>'),
                ],
            },
            {
                'name': 'Khanmigo',
                'developer': 'Khan Academy',
                'category': 'AI Tools',
                'description': '''<h3>What it is</h3>
<p>Khanmigo is a Socratic AI tutor. When a learner asks it to solve a problem, it does not hand over the answer. It asks guiding questions the way a good tutor would, so the learner does the actual thinking.</p>
<h3>What it helps you achieve</h3>
<p>Khanmigo is the strongest classroom-ready example of AI as questioner, not answer-giver. Watching it decline to give a direct answer and instead ask a guiding question is the clearest illustration of Socratic AI use as a teaching principle.</p>''',
                'website': 'https://www.khanacademy.org/khan-labs',
                'features': [
                    ('Socratic tutoring', '<p>Guides learners step by step without giving the answer.</p>', '<p><strong>How to use:</strong></p><ol><li>Set up a teacher account.</li><li>Assign a learner to Khanmigo.</li><li>Learners ask questions and are guided by follow-ups.</li></ol>'),
                    ('Teacher-side question generator', '<p>Draft practice questions aligned to a skill.</p>', '<p><strong>How to use:</strong></p><ol><li>Open the teacher dashboard.</li><li>Choose a skill.</li><li>Generate questions, review before assigning.</li></ol>'),
                    ('Conversation logs', '<p>Review learner-AI conversations.</p>', '<p><strong>How to use:</strong></p><ol><li>Open Khanmigo reports.</li><li>Click a learner.</li><li>Read the conversation for quality control.</li></ol>'),
                ],
            },
            {
                'name': 'NotebookLM',
                'developer': 'Google',
                'category': 'AI Tools',
                'description': '''<h3>What it is</h3>
<p>NotebookLM is a source-grounded AI notebook. You upload your own documents and it answers only from those documents. It will not invent something from outside what you gave it.</p>
<h3>What it helps you achieve</h3>
<p>This makes it the most academic-integrity-friendly AI tool in this week. Its answers trace back to a real source you actually uploaded. Use it to build revision material straight from your own syllabus or past papers.</p>''',
                'website': 'https://notebooklm.google.com/',
                'features': [
                    ('Upload sources', '<p>Add PDFs, Docs, slides or text.</p>', '<p><strong>How to use:</strong></p><ol><li>Create a new notebook.</li><li>Click Add Source.</li><li>Upload your documents.</li></ol>'),
                    ('Grounded Q&A', '<p>Answers cite your sources only.</p>', '<p><strong>How to use:</strong></p><ol><li>Type a question in the chat.</li><li>Click the citation to see the source passage.</li></ol>'),
                    ('Audio Overview', '<p>Podcast-style summary of your sources.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Generate Audio Overview.</li><li>Wait for the audio to process.</li><li>Share the audio link with learners.</li></ol>'),
                ],
            },
            {
                'name': 'ChatGPT, Claude, Gemini',
                'developer': 'OpenAI, Anthropic, Google',
                'category': 'AI Tools',
                'description': '''<h3>What they are</h3>
<p>The three most widely used general-purpose conversational AI assistants. Not built specifically for teachers, but useful for almost anything once you know how to ask.</p>
<h3>What they help you achieve</h3>
<p>These are your baseline prompting tools. A clear request, a follow-up refinement, and a review pass gets you a strong draft. The skill worth building is iterating, not expecting perfection on the first try.</p>''',
                'website': 'https://chat.openai.com/',
                'features': [
                    ('Baseline prompting', '<p>State role, task, format and context.</p>', '<p><strong>How to use:</strong></p><ol><li>Open a new chat.</li><li>Write: You are a (role). Help me (task) in (format). Context: (info).</li><li>Submit.</li></ol>'),
                    ('Step-by-step reasoning', '<p>Ask for step-by-step for complex tasks.</p>', '<p><strong>How to use:</strong></p><ol><li>Add Work step-by-step.</li><li>Review the chain of reasoning.</li></ol>'),
                    ('Follow-up refinement', '<p>Iterate rather than expecting perfection.</p>', '<p><strong>How to use:</strong></p><ol><li>Read the first draft.</li><li>Reply with specific edits: Shorten section 2. Simplify vocabulary.</li><li>Review again.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'AI-Assisted Lesson Pack with Corrections Documented',
            'description': '''<h3>What this assignment is about</h3>
<p>You will use at least three AI tools from this week to build a complete lesson pack, and then you will document every factual or pedagogical correction you made before the pack was ready for learners. The documentation is the more important half. It is the evidence that you used AI as a capable first-draft partner, not as a final authority.</p>
<h3>The tools you will draw from</h3>
<h4>MagicSchool AI</h4>
<p>Use it for the lesson plan draft. Give it specific context (grade, topic, standard) and treat the result as a first draft you will revise.</p>
<h4>Diffit</h4>
<p>Use it for the differentiated materials. Generate two or three reading-level versions of the same passage so a mixed-ability class can all access the content.</p>
<h4>Khanmigo, NotebookLM, or one of the general assistants</h4>
<p>Use one of these for the formative check, the reference materials, or the reflection prompts, depending on your topic. NotebookLM is the safest choice when grounded accuracy matters, because it answers only from the sources you upload.</p>
<h3>The task</h3>
<ol>
<li>Choose a topic you are about to teach.</li>
<li>Use at least three AI tools from this week to build a complete lesson pack: a plan, differentiated materials, and a formative check.</li>
<li>Then, review every output. Correct factual errors, adjust pedagogical assumptions, reword anything that does not fit your class.</li>
<li>Write a reflection of at least three hundred words documenting every correction you made, and why. If you found nothing to correct, that is a warning sign, look harder.</li>
<li>Submit the pack, the reflection, and any links to the tools you used.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A usable lesson pack and a reflection that reads like a teacher actively exercising judgement. The corrections should be specific: this fact was wrong, this activity did not match the Bloom\'s level, this example was not culturally appropriate. Generic reflections such as I reviewed it will not score well.</p>''',
            'prompt': '''<p>Submit two items:</p>
<ol>
<li>A complete AI-assisted lesson pack (plan, differentiated materials, formative check).</li>
<li>A written reflection (at least three hundred words) documenting every factual or pedagogical correction you made, and why.</li>
</ol>
<p>Ensure at least three different AI tools from this week are used, and apply the Week 10 privacy checklist to every prompt.</p>''',
            'submission_type': 'both',
            'rubric': [
                ('Tool variety', '<p>Three appropriate AI tools used purposefully.</p>', 20),
                ('Correction documentation', '<p>Specific corrections with reasoning, not vague review notes.</p>', 30),
                ('Pack quality', '<p>Materials are genuinely usable in a classroom.</p>', 25),
                ('Reflection depth', '<p>Shows judgement and discernment, not just compliance.</p>', 25),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 12
    # ------------------------------------------------------------------
    {
        'number': 12,
        'title': 'Blended and Online Pedagogy, and Leadership for Technology Adoption',
        'week_description': '''<h3>What this week is about</h3>
<p>You will learn to design a blended, flipped or fully online lesson sequence, and you will learn the change-management basics for introducing a tool or practice school-wide. The two halves fit together: a great tool poorly pitched to a skeptical director goes nowhere.</p>
<p>You will finish the week with either a blended-learning module or a one-page technology-adoption proposal suitable for presenting to a director.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Design a blended or flipped or fully online lesson sequence</li>
<li>Draft a realistic proposal for introducing a tool school-wide</li>
<li>Run an effective short training session for colleagues</li>
</ul>''',
        'topics': [
            {
                'title': 'Change Management, the ADKAR model',
                'description': '<p>Awareness, Desire, Knowledge, Ability, Reinforcement. A structured model for introducing a tool or practice to a staff room without relying on informal enthusiasm alone.</p>',
                'materials': [{'title': 'Prosci, the ADKAR model', 'content': '<p>The origin of the model and its five stages.</p>', 'url': 'https://www.prosci.com/methodology/adkar'}],
            },
        ],
        'tools': [
            {
                'name': 'Zoom',
                'developer': 'Zoom Video Communications',
                'category': 'Communication and Collaboration',
                'description': '''<h3>What it is</h3>
<p>Zoom is a live video conferencing platform for synchronous online teaching and meetings.</p>
<h3>What it helps you achieve</h3>
<p>Zoom lets you run a real class online, with breakouts, polls and recording. The session design matters far more than the software: a strong online session has a short opening explanation, a chunk of small-group work, and a debrief, not sixty minutes of you talking.</p>''',
                'website': 'https://zoom.us/',
                'features': [
                    ('Breakout rooms', '<p>Small-group discussion within a larger session.</p>', '<p><strong>How to use:</strong></p><ol><li>Start a meeting.</li><li>Click Breakout Rooms.</li><li>Choose number of rooms and assignment method.</li></ol>'),
                    ('Live polls', '<p>Check understanding mid-session.</p>', '<p><strong>How to use:</strong></p><ol><li>In-meeting, click Polls.</li><li>Launch a pre-made poll or create one live.</li><li>Share results.</li></ol>'),
                    ('Session recording', '<p>Capture sessions for absent learners.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Record, then Record to Cloud.</li><li>Get the share link after the meeting ends.</li></ol>'),
                ],
            },
            {
                'name': 'Google Meet',
                'developer': 'Google',
                'category': 'Communication and Collaboration',
                'description': '''<h3>What it is</h3>
<p>Google Meet is live video conferencing integrated with Google Workspace, so meeting links attach automatically to calendar invites.</p>
<h3>What it helps you achieve</h3>
<p>For schools already using Google Workspace, Meet removes friction: no separate accounts, no separate links, meeting links attach automatically to calendar invites.</p>''',
                'website': 'https://meet.google.com/',
                'features': [
                    ('Meeting links in Calendar', '<p>Auto-attach a Meet link to calendar invites.</p>', '<p><strong>How to use:</strong></p><ol><li>Create a Calendar event.</li><li>Click Add Google Meet conferencing.</li><li>Invitees join via the event.</li></ol>'),
                    ('Live captions', '<p>Real-time captions for accessibility.</p>', '<p><strong>How to use:</strong></p><ol><li>In-meeting, click Captions.</li><li>Choose language.</li><li>Captions appear live.</li></ol>'),
                    ('Recording to Drive', '<p>Sessions are saved directly to your Drive.</p>', '<p><strong>How to use:</strong></p><ol><li>Click Activities, then Recording.</li><li>Click Start Recording.</li></ol>'),
                ],
            },
            {
                'name': 'Microsoft Teams',
                'developer': 'Microsoft',
                'category': 'Communication and Collaboration',
                'description': '''<h3>What it is</h3>
<p>Microsoft Teams is a video conferencing and collaboration hub. For education, Class Teams gives one team per class with channels for topics.</p>
<h3>What it helps you achieve</h3>
<p>Teams brings assignments, files, chat and live meetings into one space. If your school already uses Microsoft 365, this is where your blended classroom naturally lives.</p>''',
                'website': 'https://www.microsoft.com/en-us/microsoft-teams/',
                'features': [
                    ('Class Teams', '<p>One team per class with channels for topics.</p>', '<p><strong>How to use:</strong></p><ol><li>Create a Team.</li><li>Choose Class type.</li><li>Add learners by email.</li></ol>'),
                    ('Assignments', '<p>Distribute work with due dates.</p>', '<p><strong>How to use:</strong></p><ol><li>Open Assignments in a class team.</li><li>Click Create, then Assignment.</li><li>Set the due date.</li></ol>'),
                    ('Breakout rooms', '<p>Small-group discussion in meetings.</p>', '<p><strong>How to use:</strong></p><ol><li>In-meeting, click Breakout Rooms.</li><li>Choose number and assign.</li></ol>'),
                ],
            },
        ],
        'assignment': {
            'title': 'Blended Module or Adoption Proposal',
            'description': '''<h3>What this assignment is about</h3>
<p>You will choose one of two paths. Either design a blended or flipped lesson module with a recorded walkthrough, or write a director-ready technology-adoption proposal for one tool from this course. Both paths require you to demonstrate the design thinking behind the deliverable, not just the artifact itself.</p>
<h3>The two paths</h3>
<h4>Path A, Blended module</h4>
<p>Design a lesson module in the flipped format: pre-work delivered asynchronously, in-class time used for application and support. Record a ten-minute walkthrough of the module as you would deliver it to a colleague. The walkthrough should explain every design choice: why this pre-work, why this in-class activity, how you will check completion before class starts.</p>
<h4>Path B, Adoption proposal</h4>
<p>Draft a one-page ADKAR-structured proposal for introducing one tool from this course to your school. The proposal must lead with the specific problem the tool solves, not the tool\'s features. It must propose a small, low-risk pilot with an agreed review date. It must address the five ADKAR stages explicitly: Awareness, Desire, Knowledge, Ability, Reinforcement.</p>
<h3>The tools you will draw from</h3>
<h4>Zoom, Google Meet or Microsoft Teams</h4>
<p>Choose the platform your school uses. The design matters more than the software.</p>
<h4>Edpuzzle (for Path A)</h4>
<p>Use Edpuzzle for the flipped pre-work so you have completion data before class. The rule from Week 12 is that you always check completion before class, so you can adjust if most learners did not do the pre-work.</p>
<h3>The task</h3>
<ol>
<li>Choose Path A or Path B.</li>
<li>Complete the deliverable as described above.</li>
<li>Add a short supporting document: for Path A, a completion-check plan; for Path B, the ADKAR mapping in one table.</li>
<li>Submit the deliverable plus the supporting document.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A practical, realistic deliverable a real school could adopt tomorrow. Path A should feel like something a working teacher would genuinely run. Path B should feel like something a director would sign off on. Generic theoretical documents will not score well.</p>''',
            'prompt': '''<p>Choose Path A or Path B and submit accordingly.</p>
<p><strong>Path A, Blended module:</strong></p>
<ul>
<li>Link to your recorded ten-minute walkthrough of the flipped lesson</li>
<li>A one-page completion-check plan</li>
</ul>
<p><strong>Path B, Adoption proposal:</strong></p>
<ul>
<li>Link to your one-page ADKAR-structured proposal</li>
<li>A one-page ADKAR mapping table showing how each stage is addressed</li>
</ul>''',
            'submission_type': 'both',
            'rubric': [
                ('Path chosen and justified', '<p>Either module or proposal clearly chosen.</p>', 20),
                ('Structure', '<p>Path A fits the flipped model; Path B follows ADKAR.</p>', 30),
                ('Realism', '<p>Practical for a real school context.</p>', 25),
                ('Quality', '<p>Presentation-ready for its audience.</p>', 25),
            ],
        },
    },
    # ------------------------------------------------------------------
    # WEEK 13
    # ------------------------------------------------------------------
    {
        'number': 13,
        'title': 'Practicum, Peer Critique, Research-Based Evaluation and Capstone Defense',
        'week_description': '''<h3>What this week is about</h3>
<p>This is the synthesis week. There are no new tools. Everything you have learned across twelve weeks is pulled together into a capstone portfolio that demonstrates your practical command of pedagogy, technology and classroom execution. You will also learn to give and receive structured peer feedback, and to evaluate EdTech research with a skeptical eye.</p>
<p>Certification is issued on the portfolio, not on attendance. This is the assignment that matters most.</p>
<h3>By the end of this week you will be able to</h3>
<ul>
<li>Teach or record a full technology-integrated lesson</li>
<li>Critique peers using a shared, published rubric</li>
<li>Evaluate an EdTech efficacy claim against independent evidence</li>
</ul>''',
        'topics': [
            {
                'title': 'Structured Peer Observation Protocol',
                'description': '<p>A shared rubric-based protocol for giving and receiving feedback that is specific and evidence-based rather than impressionistic. Observe, score against a shared rubric, self-score, then compare and discuss the gap.</p>',
                'materials': [{'title': 'Triple E Framework, rubric reference', 'content': '<p>Used as part of the shared rubric alongside SAMR and UDL.</p>', 'url': 'https://www.tripleeframework.com/'}],
            },
            {
                'title': 'Reading and Evaluating EdTech Research',
                'description': '<p>A basic framework for judging whether an EdTech efficacy claim is credible before adopting a tool based on it. Distinguish a specific, falsifiable evidence claim from a vague enthusiasm claim.</p>',
                'materials': [{'title': 'Education Endowment Foundation, Teaching and Learning Toolkit', 'content': '<p>Summarises education-intervention research by average impact and evidence strength. Check this before adopting a tool based on a marketing claim.</p>', 'url': 'https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit'}],
            },
            {
                'title': 'Capstone Portfolio Assembly',
                'description': '<p>The final synthesis. A complete portfolio draws from every part of the certificate: a backward-designed unit, tool-integrated materials from Weeks 4 to 7, an AI-assisted lesson pack from Week 11, and a taught or recorded lesson with peer review.</p>',
                'materials': [{'title': 'CAST, UDL Guidelines, rubric reference', 'content': '<p>Used as one of the framework references for the portfolio reflective memo.</p>', 'url': 'https://udlguidelines.cast.org/'}],
            },
        ],
        'tools': [],
        'assignment': {
            'title': 'Capstone Portfolio',
            'description': '''<h3>What this assignment is about</h3>
<p>The capstone portfolio is the assessed deliverable of the entire certificate. It is not a single test. It is a body of evidence showing that you can plan, build, teach and reflect on a technology-integrated lesson. A complete portfolio draws from every part of the certificate, and it is what certification is based on.</p>
<h3>The frameworks you will draw from</h3>
<h4>Backward Design (Week 3)</h4>
<p>Your unit plan is the structural spine of the portfolio. It should be the same plan you designed in Week 3, refined since then.</p>
<h4>SAMR, TPACK, UDL (Week 2)</h4>
<p>Your reflective memo must connect specific choices back to these frameworks. Not as name-drops, but as explanations of specific decisions you made.</p>
<h4>AI-assisted lesson pack (Week 11)</h4>
<p>Your AI pack, with the corrections documented, becomes one of the artifacts.</p>
<h4>Peer observation and feedback (this week)</h4>
<p>Your recorded or observed lesson, and the peer-observation comparison, become another artifact.</p>
<h3>The task</h3>
<ol>
<li>Assemble five components: the backward-designed unit plan, at least one artifact each from Weeks 4, 5, 6 and 7, the AI-assisted lesson pack from Week 11, a taught or recorded lesson with peer-observation feedback, and a reflective memo.</li>
<li>Write a one-page reflective memo connecting your choices back to Bloom\'s, Multiple Intelligences, SAMR and UDL. Every framework named should explain a specific decision you made.</li>
<li>Assemble everything into a single, clearly organised submission (Google Drive folder, PDF, or similar).</li>
<li>Submit the link.</li>
</ol>
<h3>What a good submission looks like</h3>
<p>A portfolio that reads as a genuine body of work, not a scrapbook of unrelated files. The reflective memo is the centrepiece: it should be the piece of writing that proves you understand not just how to use the tools, but why they work. This is what a postgraduate qualification would ask of you, and this portfolio should meet that standard.</p>''',
            'prompt': '''<p>Submit a single shareable link to your assembled capstone portfolio. It must include:</p>
<ol>
<li>Your backward-designed unit plan from Week 3</li>
<li>At least one artifact each from Weeks 4, 5, 6 and 7</li>
<li>Your AI-assisted lesson pack from Week 11, with corrections documented</li>
<li>A taught or recorded lesson, plus your completed peer-observation comparison</li>
<li>A one-page reflective memo connecting your choices to Bloom\'s, Multiple Intelligences, SAMR and UDL</li>
</ol>''',
            'submission_type': 'link',
            'rubric': [
                ('Completeness', '<p>All five components present.</p>', 20),
                ('Evidence quality', '<p>Artifacts are the real, corrected work.</p>', 25),
                ('Reflection memo', '<p>Frameworks applied to genuine decisions, not listed.</p>', 30),
                ('Overall presentation', '<p>Certification-ready quality.</p>', 25),
            ],
        },
    },
]


class Command(BaseCommand):
    help = 'Seed the full thirteen-week curriculum with topics, tools, features and assignments.'

    def add_arguments(self, parser):
        parser.add_argument('--cohort', type=str, default='September 2026 Cohort')
        parser.add_argument('--reset', action='store_true', help='Delete existing weeks for this cohort before seeding.')

    @transaction.atomic
    def handle(self, *args, **options):
        cohort, _ = Cohort.objects.get_or_create(
            name=options['cohort'],
            defaults={
                'start_date': date(2026, 9, 1),
                'description': '<p>Full thirteen-week certificate cohort.</p>',
            },
        )
        self.stdout.write(f'Cohort: {cohort.name}')

        if options['reset']:
            self.stdout.write(self.style.WARNING('Deleting existing weeks for this cohort...'))
            Week.objects.filter(cohort=cohort).delete()

        for week_data in WEEKS:
            week, created = Week.objects.get_or_create(
                cohort=cohort,
                number=week_data['number'],
                defaults={
                    'title': week_data['title'],
                    'description': week_data['week_description'],
                },
            )
            if not created:
                week.title = week_data['title']
                week.description = week_data['week_description']
                week.save()
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} Week {week.number}: {week.title}')

            for t_order, topic_data in enumerate(week_data.get('topics', []), start=1):
                topic, _ = Topic.objects.update_or_create(
                    week=week,
                    title=topic_data['title'],
                    defaults={
                        'description': topic_data.get('description', ''),
                        'order': t_order,
                    },
                )
                for m_order, mat in enumerate(topic_data.get('materials', []), start=1):
                    ReferenceMaterial.objects.update_or_create(
                        topic=topic,
                        title=mat['title'],
                        defaults={
                            'content': mat.get('content', ''),
                            'url': mat.get('url', ''),
                            'order': m_order,
                        },
                    )

            for tool_order, tool_data in enumerate(week_data.get('tools', []), start=1):
                tool, _ = Tool.objects.update_or_create(
                    week=week,
                    name=tool_data['name'],
                    defaults={
                        'developer': tool_data.get('developer', ''),
                        'category': tool_data.get('category', ''),
                        'description': tool_data.get('description', ''),
                        'website': tool_data.get('website', ''),
                        'order': tool_order,
                    },
                )
                for f_order, (title, purpose_html, how_html) in enumerate(tool_data.get('features', []), start=1):
                    ToolFeature.objects.update_or_create(
                        tool=tool,
                        title=title,
                        defaults={
                            'purpose': purpose_html,
                            'how_to_use': how_html,
                            'order': f_order,
                        },
                    )

            a_data = week_data.get('assignment')
            if a_data:
                assignment, _ = Assignment.objects.update_or_create(
                    week=week,
                    title=a_data['title'],
                    defaults={
                        'description': a_data.get('description', ''),
                        'prompt': a_data.get('prompt', ''),
                        'submission_type': a_data.get('submission_type', 'link'),
                        'is_open_ended': True,
                        'tool': None,
                    },
                )
                for r_order, (name, desc_html, max_score) in enumerate(a_data.get('rubric', []), start=1):
                    RubricCriterion.objects.update_or_create(
                        assignment=assignment,
                        name=name,
                        defaults={
                            'description': desc_html,
                            'max_score': max_score,
                            'order': r_order,
                        },
                    )

        self.stdout.write(self.style.SUCCESS('Full curriculum seeded.'))
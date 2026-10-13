from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.learning.models import (
    Cohort, Week, Topic, ReferenceMaterial, Tool, ToolFeature,
    Assignment, RubricCriterion
)


# -------------------------------------------------------------
# Curriculum data: weeks → topics, tools, assignments
# -------------------------------------------------------------

WEEKS = [
    {
        'number': 1,
        'title': 'Orientation, Diagnostic & Comparative Curriculum Literacy',
        'description': 'Set up your practice journal and map your curriculum against the others in the room.',
        'topics': [
            {
                'title': 'Comparative Curriculum Reference — CBE, IGCSE, IB, BNC, American',
                'description': 'A single reference point for translating any activity into the language and structure of five curricula.',
                'materials': [
                    {
                        'title': 'Curriculum Alignment Reference',
                        'content': 'The domains below are common across CBE, IGCSE, IB, BNC, and American curricula: Language & Literacy, Mathematics, Sciences, Humanities/Social Studies, Digital Literacy/ICT, Creative & Physical Education. Names differ ("strand," "subject group," "standard"), but the underlying question is the same: what should a learner know and be able to do by a given point?',
                        'url': 'https://kicd.ac.ke/',
                    },
                    {
                        'title': 'Cambridge International — Syllabuses',
                        'content': 'Cambridge organises by subject syllabus with assessment objectives.',
                        'url': 'https://www.cambridgeinternational.org/',
                    },
                    {
                        'title': 'IB Organization',
                        'content': 'IB is concept- and inquiry-driven, organised around Approaches to Learning (ATL) and Learner Profile attributes.',
                        'url': 'https://www.ibo.org/',
                    },
                ],
            },
        ],
        'tools': [
            {
                'name': 'Microsoft Word',
                'developer': 'Microsoft Corporation',
                'category': 'Productivity',
                'description': 'Word processing and structured document creation for lesson/unit plans and journals.',
                'website': 'https://www.microsoft.com/en-us/microsoft-365/word',
                'features': [
                    ('Styles & Headings',
                     'Create consistent, navigable document structure and automatic tables of contents.',
                     '1. Open a document.\n2. Go to the Home tab.\n3. Select the text and apply Heading 1, Heading 2 from the Styles gallery.\n4. Use References > Table of Contents to insert an automatic TOC.'),
                    ('Track Changes',
                     'Enable visible, reversible peer or supervisor feedback on a document.',
                     '1. Open the Review tab.\n2. Click Track Changes.\n3. Share the document.\n4. Every edit appears as a change; use Accept/Reject to finalise.'),
                    ('Tables & Rubrics',
                     'Build structured tables such as rubrics or comparison grids.',
                     '1. Go to Insert > Table.\n2. Choose rows/columns.\n3. Enter your criteria and performance levels.\n4. Apply Table Styles for readability.'),
                ],
            },
            {
                'name': 'Google Docs',
                'developer': 'Google',
                'category': 'Productivity',
                'description': 'Free, browser-based word processing with real-time collaboration.',
                'website': 'https://docs.google.com/',
                'features': [
                    ('Real-time Co-editing',
                     'Multiple people type into the same document simultaneously, each visible live.',
                     '1. Open a Doc.\n2. Click Share.\n3. Add collaborators by email.\n4. Each cursor appears in a distinct colour.'),
                    ('Comment & Suggesting Mode',
                     'Leave comments or propose edits that the author can accept or reject.',
                     '1. Select text.\n2. Click Insert > Comment (Ctrl+Alt+M).\n3. Or switch to Suggesting mode from the top-right dropdown.'),
                    ('Version History',
                     'See every change ever made and restore any prior version.',
                     '1. Click File > Version history > See version history.\n2. Choose a timestamp.\n3. Click Restore.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Curriculum Alignment Worksheet',
                'description': 'Produce a one-page Curriculum Alignment Worksheet for your subject.',
                'prompt': 'List the subject/learning area you teach. Locate its equivalent name and structure in your curriculum\'s official documentation. Identify the closest-matching strand in at least two other curricula. Note one point of genuine difference (not just wording). Submit a link to your completed worksheet (Word or Google Doc).',
                'submission_type': 'link',
                'rubric': [
                    ('Coverage', 'All five curricula addressed', 20),
                    ('Accuracy', 'Structures correctly identified', 25),
                    ('Cross-curriculum insight', 'Genuine difference noted, not just wording', 25),
                    ('Reflection', 'Personal teaching note attached', 30),
                ],
            },
        ],
    },
    {
        'number': 2,
        'title': 'Learning Theory & Technology-Integration Frameworks',
        'description': 'Bloom\'s, Multiple Intelligences, TPACK, SAMR, UDL, Triple E.',
        'topics': [
            {
                'title': 'Bloom\'s Taxonomy (Revised)',
                'description': 'Six levels of cognitive demand: Remember, Understand, Apply, Analyze, Evaluate, Create.',
                'materials': [
                    {'title': 'Bloom\'s reference', 'content': 'Origin: Benjamin Bloom (1956); revised by Anderson & Krathwohl (2001). Used as the standard language for every tool\'s pedagogical foundation in this course.', 'url': 'https://cft.vanderbilt.edu/guides-sub-pages/blooms-taxonomy/'},
                ],
            },
            {
                'title': 'Gardner\'s Multiple Intelligences',
                'description': 'Eight ways people process information: Linguistic, Logical-Mathematical, Spatial, Bodily-Kinesthetic, Musical, Interpersonal, Intrapersonal, Naturalistic.',
                'materials': [
                    {'title': 'Multiple Intelligences reference', 'content': 'Origin: Howard Gardner (1983). Use as a planning-variety checklist, not a fixed label for individual learners.', 'url': 'https://pz.harvard.edu/'},
                ],
            },
            {
                'title': 'TPACK — The Master Framework',
                'description': 'Technological, Pedagogical, and Content Knowledge must intersect for sound tech choice.',
                'materials': [
                    {'title': 'TPACK reference', 'content': 'Origin: Punya Mishra and Matthew Koehler (2006). Before selecting any tool, state your content goal, then your pedagogy, then choose the technology that serves both.', 'url': 'https://tpack.org/'},
                ],
            },
            {
                'title': 'SAMR Model',
                'description': 'Substitution, Augmentation, Modification, Redefinition — Enhancement vs Transformation.',
                'materials': [
                    {'title': 'SAMR reference', 'content': 'Origin: Dr. Ruben Puentedura (2010). Not a demand that every lesson reach Redefinition; a habit of asking the question.', 'url': 'https://www.schrockguide.net/samr.html'},
                ],
            },
            {
                'title': 'Universal Design for Learning (UDL)',
                'description': 'Multiple means of Engagement, Representation, and Action & Expression.',
                'materials': [
                    {'title': 'UDL Guidelines', 'content': 'Origin: CAST. Design flexibility in from the start; the content stays the same, access points multiply.', 'url': 'https://udlguidelines.cast.org/'},
                ],
            },
            {
                'title': 'Triple E Framework',
                'description': 'Engage, Enhance, Extend — is this actually good for learning?',
                'materials': [
                    {'title': 'Triple E reference', 'content': 'Origin: Dr. Liz Kolb, University of Michigan. Ask: does the tool Engage learners in the learning goal, Enhance what would be hard without it, Extend beyond the classroom?', 'url': 'https://www.tripleeframework.com/'},
                ],
            },
        ],
        'tools': [],
        'assignments': [
            {
                'title': 'SAMR/TPACK Analysis of Your Lesson',
                'description': 'Analyse one of your own existing lessons through both frameworks.',
                'prompt': 'Choose one lesson you currently teach. Write the TPACK triad (content, pedagogy, technology) as three sentences. Then classify the lesson on the SAMR ladder and justify the level with concrete evidence. Submit a link to your written analysis (at least 500 words).',
                'submission_type': 'link',
                'rubric': [
                    ('TPACK triad clarity', 'Content, pedagogy, technology clearly stated', 25),
                    ('SAMR level accuracy', 'Correct level identified with evidence', 30),
                    ('Critical reflection', 'Beyond description, shows insight', 25),
                    ('Structure & clarity', 'Well organised, easy to read', 20),
                ],
            },
        ],
    },
    {
        'number': 3,
        'title': 'Instructional & Learning Design',
        'description': 'Backward Design and ADDIE — plan the finish line first.',
        'topics': [
            {
                'title': 'Backward Design (Understanding by Design)',
                'description': 'Three stages: identify desired results, determine acceptable evidence, plan learning experiences.',
                'materials': [
                    {'title': 'Backward Design reference', 'content': 'Origin: Wiggins & McTighe (1998). Assessment evidence is designed before any activity is planned.', 'url': 'https://cft.vanderbilt.edu/guides-sub-pages/understanding-by-design/'},
                ],
            },
            {
                'title': 'ADDIE Model',
                'description': 'Analyze, Design, Develop, Implement, Evaluate — cyclical.',
                'materials': [
                    {'title': 'ADDIE reference', 'content': 'Developed for U.S. military/corporate training in the 1970s. Evaluate feeds back into Analyze for the next cycle.', 'url': 'https://www.instructionaldesign.org/models/addie/'},
                ],
            },
        ],
        'tools': [
            {
                'name': 'Microsoft Excel',
                'developer': 'Microsoft Corporation',
                'category': 'Productivity',
                'description': 'Spreadsheet for gradebooks, scope-and-sequence mapping, and data analysis.',
                'website': 'https://www.microsoft.com/en-us/microsoft-365/excel',
                'features': [
                    ('Conditional Formatting',
                     'Automatically flag learners below a mastery threshold.',
                     '1. Select the score column.\n2. Home > Conditional Formatting > Highlight Cells Rules.\n3. Choose "Less Than" and enter 50%.\n4. Pick a red fill.'),
                    ('Pivot Tables',
                     'Summarize a term of scattered scores into one pattern.',
                     '1. Select your data.\n2. Insert > PivotTable.\n3. Drag fields to Rows, Columns, Values.\n4. Refresh when source data changes.'),
                    ('Charts',
                     'Visualize class trends for staff or parent meetings.',
                     '1. Select the data range.\n2. Insert > Chart.\n3. Choose bar, line, or pie.\n4. Use Chart Design to refine.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Backward-Designed Unit Plan',
                'description': 'One fully backward-designed unit plan in your own subject.',
                'prompt': 'Choose an upcoming unit. Write it in the three Backward Design stages: (1) desired result, (2) assessment evidence, (3) learning activities. Submit a link to your plan (Google Doc or Word). Activities must not begin until evidence is defined.',
                'submission_type': 'link',
                'rubric': [
                    ('Desired result', 'Clear, measurable, high-cognition', 25),
                    ('Assessment evidence', 'Genuinely proves the result', 25),
                    ('Activities alignment', 'Activities lead to the evidence', 30),
                    ('UDL differentiation', 'Multiple means of representation/expression', 20),
                ],
            },
        ],
    },
    {
        'number': 4,
        'title': 'Productivity & Documentation Mastery',
        'description': 'Word, Excel, PowerPoint, Google Workspace, scheduling, digital notebooks.',
        'topics': [],
        'tools': [
            {
                'name': 'Microsoft PowerPoint',
                'developer': 'Microsoft Corporation',
                'category': 'Productivity',
                'description': 'Presentation software with Slide Master for consistent design.',
                'website': 'https://www.microsoft.com/en-us/microsoft-365/powerpoint',
                'features': [
                    ('Slide Master',
                     'Set a consistent professional design across the whole deck.',
                     '1. View > Slide Master.\n2. Edit the master slide (fonts, colours, logo).\n3. Close Master View. Every slide inherits the design.'),
                    ('Purposeful Animation',
                     'Reveal information in a planned sequence.',
                     '1. Select an object.\n2. Animations tab.\n3. Choose Appear, Fade, or Wipe.\n4. Set Start: On Click or With Previous.'),
                    ('Export as Video',
                     'Repurpose a lesson deck as an asynchronous resource.',
                     '1. File > Export > Create a Video.\n2. Choose quality.\n3. Set timing.\n4. Click Create Video.'),
                ],
            },
            {
                'name': 'Google Workspace for Education',
                'developer': 'Google',
                'category': 'Productivity',
                'description': 'Cloud-based productivity suite — Docs, Sheets, Slides, Classroom.',
                'website': 'https://workspace.google.com/education/',
                'features': [
                    ('Google Classroom',
                     'Centralize assignments and communication per class.',
                     '1. Go to classroom.google.com.\n2. Click + > Create class.\n3. Share the class code.\n4. Post assignments via Classwork tab.'),
                    ('Sheets Formulas',
                     'Calculate totals and averages automatically.',
                     '1. Click a cell.\n2. Type =SUM(A1:A10) or =AVERAGE(A1:A10).\n3. Press Enter. Values update live.'),
                    ('Real-time Collaboration',
                     'Multiple learners edit one document simultaneously.',
                     '1. Open a Doc.\n2. Share with edit rights.\n3. Watch cursors appear live.\n4. Use Comments to discuss.'),
                ],
            },
            {
                'name': 'OneNote',
                'developer': 'Microsoft',
                'category': 'Productivity',
                'description': 'Digital notebook for capturing learner observations across devices.',
                'website': 'https://www.onenote.com/',
                'features': [
                    ('Notebook per Class',
                     'Organise planning notes, observations, and resources.',
                     '1. File > New Notebook.\n2. Create sections: Planning, Observations, Resources.\n3. Add pages within each section.'),
                    ('Tags',
                     'Mark items needing follow-up.',
                     '1. Select a note.\n2. Home > Tags > To Do (or create a custom tag).\n3. Use Find Tags to review all tagged items.'),
                    ('Cross-device Sync',
                     'Capture on phone, review on laptop.',
                     '1. Install OneNote on phone and laptop.\n2. Sign in with the same Microsoft account.\n3. Notes sync automatically.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Build a Working Gradebook',
                'description': 'A functioning gradebook with conditional formatting and charts.',
                'prompt': 'Build a gradebook for one class in Excel or Google Sheets. Include at least 8 learners and 3 assessments. Add conditional formatting that flags any learner below 50%. Add one chart showing class trends. Submit a link to your spreadsheet (shareable view-only).',
                'submission_type': 'link',
                'rubric': [
                    ('Formulas correct', 'Averages and totals compute correctly', 25),
                    ('Conditional formatting', 'Flags below-threshold learners automatically', 25),
                    ('Chart clarity', 'Chart is readable and labelled', 25),
                    ('Professional presentation', 'Clean, usable by another teacher', 25),
                ],
            },
            {
                'title': 'Lesson Slide Deck',
                'description': 'A five-slide lesson using Slide Master.',
                'prompt': 'Build a five-slide lesson deck using a single Slide Master theme. Include one purposeful animation sequence. Export as a short video and submit the link.',
                'submission_type': 'link',
                'rubric': [
                    ('Slide Master applied', 'Consistent design throughout', 25),
                    ('Content organisation', 'One core idea per slide', 25),
                    ('Purposeful animation', 'Sequencing, not decoration', 25),
                    ('Video export quality', 'Clear audio/visual', 25),
                ],
            },
        ],
    },
    {
        'number': 5,
        'title': 'Visual & Multimedia Content Creation',
        'description': 'Canva, H5P, Book Creator, Edpuzzle, Loom.',
        'topics': [],
        'tools': [
            {
                'name': 'Canva for Education',
                'developer': 'Canva Pty Ltd',
                'category': 'Visual & Multimedia',
                'description': 'Graphic design and multimedia creation — free for verified educators.',
                'website': 'https://www.canva.com/education/',
                'features': [
                    ('Templates Library',
                     'Start fast with pre-made professional designs.',
                     '1. Log in to Canva.\n2. Search "worksheet" or "infographic".\n3. Pick a template.\n4. Edit text and images.'),
                    ('Brand Kit',
                     'Keep school colours and logos consistent.',
                     '1. Click Brand Kit in the sidebar.\n2. Upload your logo.\n3. Add brand colours and fonts.\n4. Apply across all designs.'),
                    ('Classroom Assignments',
                     'Assign design tasks directly to learners.',
                     '1. Go to Classroom tab.\n2. Click Create assignment.\n3. Select Canva template.\n4. Share with your class.'),
                ],
            },
            {
                'name': 'H5P',
                'developer': 'Joubel',
                'category': 'Visual & Multimedia',
                'description': 'Interactive content authoring — free and open-source.',
                'website': 'https://h5p.org/',
                'features': [
                    ('Interactive Video',
                     'Embed questions at specific timestamps in a video.',
                     '1. Choose Interactive Video in H5P editor.\n2. Upload or paste a video URL.\n3. Add interaction points at timestamps.\n4. Insert multiple-choice or open questions.'),
                    ('Course Presentation',
                     'Build a slide deck with embedded quizzes.',
                     '1. Choose Course Presentation.\n2. Add slides with text, images, video.\n3. Insert quiz slides between content.\n4. Publish and embed in your LMS.'),
                    ('Drag the Words',
                     'Learners drag missing words into a sentence.',
                     '1. Choose Drag the Words.\n2. Enter your text with *markers* for gaps.\n3. Set options.\n4. Publish.'),
                ],
            },
            {
                'name': 'Edpuzzle',
                'developer': 'Edpuzzle, Inc.',
                'category': 'Visual & Multimedia',
                'description': 'Interactive video with embedded questions.',
                'website': 'https://edpuzzle.com/',
                'features': [
                    ('Video Trimming',
                     'Cut a video to just the relevant section.',
                     '1. Upload or search for a video.\n2. Use the crop tool to trim start/end.\n3. Preview.'),
                    ('Embedded Questions',
                     'Insert multiple-choice or open-ended questions at timestamps.',
                     '1. Click the question icon in the editor.\n2. Choose question type.\n3. Write the question.\n4. Drag to position on the timeline.'),
                    ('Completion Reports',
                     'See which questions the class struggled with.',
                     '1. Assign to a class.\n2. Open the Reports tab.\n3. Filter by question or learner.'),
                ],
            },
            {
                'name': 'Loom',
                'developer': 'Loom, Inc.',
                'category': 'Visual & Multimedia',
                'description': 'Screen and webcam recording for short explainer videos.',
                'website': 'https://www.loom.com/',
                'features': [
                    ('Screen + Webcam Recording',
                     'Record your screen and face simultaneously.',
                     '1. Install Loom extension.\n2. Click the Loom icon.\n3. Choose screen + cam.\n4. Click Start Recording.'),
                    ('Instant Share Link',
                     'No upload required — a link is generated automatically.',
                     '1. Stop recording.\n2. The share link is copied to your clipboard.\n3. Paste anywhere.'),
                    ('Trim & Chapters',
                     'Cut the start/end and add chapter markers.',
                     '1. Open a recording in Loom.\n2. Click Trim.\n3. Add chapter titles in the editor.'),
                ],
            },
            {
                'name': 'Book Creator',
                'developer': 'Red Jumper Studio',
                'category': 'Visual & Multimedia',
                'description': 'Learner-authoring tool for multimedia digital books.',
                'website': 'https://bookcreator.com/',
                'features': [
                    ('Page Templates',
                     'Choose comic, portrait, or square layouts.',
                     '1. Create a new book.\n2. Choose a page template.\n3. Add pages as you go.'),
                    ('Audio Narration',
                     'Learners record their own voice per page.',
                     '1. Open a page.\n2. Click the + icon.\n3. Select Audio.\n4. Record, then place on page.'),
                    ('Class Library Publishing',
                     'Share completed books with the whole class.',
                     '1. Click the publish icon.\n2. Choose Publish to Library.\n3. Classmates can read and comment.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Multimedia Lesson Pack',
                'description': 'A Canva resource + an Edpuzzle video lesson.',
                'prompt': 'Create one Canva resource (worksheet, infographic, or poster) for a topic you teach. Then take an existing video on the same topic and embed at least 4 comprehension questions using Edpuzzle. Submit a link to both.',
                'submission_type': 'both',
                'rubric': [
                    ('Canva design quality', 'Professional, on-brand, readable', 25),
                    ('Edpuzzle question quality', 'Questions check real comprehension', 25),
                    ('Topic alignment', 'Both resources serve the same learning goal', 25),
                    ('Written reflection', 'Notes on what each resource adds', 25),
                ],
            },
        ],
    },
    {
        'number': 6,
        'title': 'Interactive & Collaborative Classroom Tools',
        'description': 'Nearpod, Pear Deck, Padlet, Miro, Kahoot!, Wayground, Socrative, Plickers.',
        'topics': [],
        'tools': [
            {
                'name': 'Nearpod',
                'developer': 'Renaissance Learning',
                'category': 'Interactive & Collaborative',
                'description': 'Interactive slide-based lesson delivery.',
                'website': 'https://nearpod.com/',
                'features': [
                    ('Interactive Slides',
                     'Insert polls, open questions, and drawing boards between content.',
                     '1. Upload an existing deck or build new.\n2. Click Add Slide > Interactive.\n3. Choose Poll, Open-Ended, Draw It, or Quiz.'),
                    ('Teacher-Paced vs Student-Paced',
                     'Choose live-together or independent work.',
                     '1. After building, click Live Participation for whole-class, or Student-Paced for independent.'),
                    ('Post-Session Reports',
                     'See which learners need follow-up.',
                     '1. After the session, open Reports.\n2. Sort by learner or by question.\n3. Note low performers for re-teach.'),
                ],
            },
            {
                'name': 'Padlet',
                'developer': 'Padlet',
                'category': 'Interactive & Collaborative',
                'description': 'Collaborative digital board — Wall, Map, Timeline layouts.',
                'website': 'https://padlet.com/',
                'features': [
                    ('Multiple Layouts',
                     'Choose the format that fits the task.',
                     '1. Click Make a Padlet.\n2. Choose Wall, Grid, Shelf, Map, or Timeline.\n3. Set your title and description.'),
                    ('Posting Permissions',
                     'Anonymous or named, editable or view-only.',
                     '1. In the settings, click Privacy.\n2. Choose who can post.\n3. Optionally allow anonymous posts.'),
                    ('QR-code Sharing',
                     'Share instantly in low-device classrooms.',
                     '1. Click Share in the top-right.\n2. Click the QR icon.\n3. Project it — learners scan and post.'),
                ],
            },
            {
                'name': 'Miro',
                'developer': 'Miro',
                'category': 'Interactive & Collaborative',
                'description': 'Collaborative online whiteboard with distinct cursors per learner.',
                'website': 'https://miro.com/',
                'features': [
                    ('Templates',
                     'Mind maps, KWL charts, brainstorm grids ready-made.',
                     '1. Click New Board.\n2. Choose from Templates gallery.\n3. Apply and edit.'),
                    ('Sticky Notes & Shapes',
                     'Real-time brainstorming with trackable contributions.',
                     '1. Press N for a sticky note.\n2. Type and place.\n3. Each learner\'s cursor is a different colour.'),
                    ('Export to PDF',
                     'Save the finished board as a class record.',
                     '1. Click Export this board.\n2. Choose PDF or image.\n3. Save or share.'),
                ],
            },
            {
                'name': 'Kahoot!',
                'developer': 'Kahoot! ASA',
                'category': 'Interactive & Collaborative',
                'description': 'Live gamified quiz for rapid recall review.',
                'website': 'https://kahoot.com/',
                'features': [
                    ('Quiz Builder',
                     'Create or adapt multiple-choice quizzes.',
                     '1. Click Create.\n2. Add questions and answers.\n3. Set timing and points.'),
                    ('Live Hosting',
                     'Project the quiz; learners answer on their own devices.',
                     '1. Click Play.\n2. Choose Classic or Team Mode.\n3. Share the game PIN.'),
                    ('Per-Question Reports',
                     'See which question the class struggled with most.',
                     '1. After the session, open Reports.\n2. Click the question to see accuracy.'),
                ],
            },
            {
                'name': 'Plickers',
                'developer': 'Plickers, Inc.',
                'category': 'Interactive & Collaborative',
                'description': 'Low-device formative assessment using printed cards — only the teacher needs a device.',
                'website': 'https://plickers.com/',
                'features': [
                    ('Printed Cards',
                     'Free printable PDF for the whole class.',
                     '1. Log in to Plickers.com.\n2. Go to Classes > Print Cards.\n3. Print one card per learner.'),
                    ('Question Sets',
                     'Create multiple-choice questions in the app.',
                     '1. Go to Library > New Question.\n2. Add text and 4 answer choices.\n3. Assign to a class.'),
                    ('Phone Scan',
                     'Capture the whole class\'s answers instantly.',
                     '1. Open the Plickers app on your phone.\n2. Select a question.\n3. Scan the room with the camera.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Interactive Lesson Delivery',
                'description': 'One fully interactive lesson using at least three tools from this week.',
                'prompt': 'Design and deliver (or record) one lesson using at least three tools from this week (e.g. Nearpod + Padlet + Kahoot!). Submit a link to a screen recording of the lesson AND a short written reflection on what each tool contributed.',
                'submission_type': 'both',
                'rubric': [
                    ('Tool variety', 'Three different tools used purposefully', 25),
                    ('Pedagogical fit', 'Each tool fits the pedagogical moment', 25),
                    ('Learner engagement', 'Evidence of learner participation', 25),
                    ('Written reflection', 'Insightful, specific to the lesson', 25),
                ],
            },
        ],
    },
    {
        'number': 7,
        'title': 'Gamification & Game-Based Learning',
        'description': 'Gimkit, Classcraft, Prodigy, Duolingo, Minecraft Education, CodeCombat, Quizlet, Brainscape.',
        'topics': [
            {
                'title': 'Governing principle',
                'description': 'A mechanic is only worth using if it reinforces a specific, stated learning objective.',
                'materials': [
                    {'title': 'Chocolate-covered broccoli', 'content': 'Engagement without a tied objective is decoration, not pedagogy. Verify content-level mastery, not just fun.', 'url': ''},
                ],
            },
        ],
        'tools': [
            {
                'name': 'Gimkit',
                'developer': 'Gimkit, Inc.',
                'category': 'Gamification',
                'description': 'Game-show style quiz with an in-game economy.',
                'website': 'https://www.gimkit.com/',
                'features': [
                    ('Kits',
                     'Build or import question sets.',
                     '1. Click Create.\n2. Add questions or import from a quiz file.\n3. Save as a "kit".'),
                    ('Team Mode',
                     'Collaborative spending decisions add a strategy layer.',
                     '1. Click Play.\n2. Choose Team Mode.\n3. Assign learners to teams.'),
                    ('In-game Economy',
                     'Learners spend earned currency on power-ups.',
                     '1. Learners earn cash per correct answer.\n2. They open the Shop mid-game.\n3. Purchase power-ups strategically.'),
                ],
            },
            {
                'name': 'Quizlet',
                'developer': 'Quizlet, Inc.',
                'category': 'Gamification',
                'description': 'Flashcard platform with Match and Gravity game modes.',
                'website': 'https://quizlet.com/',
                'features': [
                    ('Study Sets',
                     'Create term/definition pairs.',
                     '1. Click Create.\n2. Enter terms and definitions.\n3. Save the set.'),
                    ('Match Game',
                     'Timed pairing of terms and definitions.',
                     '1. Open a set.\n2. Choose Match.\n3. Race to clear the board.'),
                    ('Quizlet Live',
                     'Real-time team-based review.',
                     '1. Open a set.\n2. Click Live.\n3. Share the join code with the class.'),
                ],
            },
            {
                'name': 'CodeCombat',
                'developer': 'CodeCombat, Inc.',
                'category': 'Gamification',
                'description': 'Game-based real coding instruction — Python and JavaScript.',
                'website': 'https://codecombat.com/',
                'features': [
                    ('Course Levels',
                     'Assign based on prior experience.',
                     '1. Create a class.\n2. Assign learners to a course level.\n3. Track progress by level.'),
                    ('Real Code Entry',
                     'Learners write genuine Python or JavaScript.',
                     '1. Open a level.\n2. Type code in the editor.\n3. Click Run.'),
                    ('Teacher Dashboard',
                     'See exactly which line each learner is stuck on.',
                     '1. Open your class dashboard.\n2. Click a learner.\n3. View the specific line of code they last ran.'),
                ],
            },
            {
                'name': 'Quizlet',
                'developer': 'Quizlet, Inc.',
                'category': 'Gamification',
                'description': 'Flashcards with game modes.',
                'website': 'https://quizlet.com/',
                'features': [
                    ('Learn Mode', 'Adaptive spaced practice.', '1. Open a set.\n2. Click Learn.\n3. Answer questions as they resurface.'),
                    ('Gravity', 'Fast typing game for review.', '1. Open a set.\n2. Click Gravity.\n3. Type answers before asteroids hit.'),
                    ('Live Reports', 'See per-term accuracy.', '1. After a Live session, open Reports.\n2. Note low-accuracy terms for re-teach.'),
                ],
            },
            {
                'name': 'Brainscape',
                'developer': 'Brainscape LLC',
                'category': 'Gamification',
                'description': 'Spaced-repetition flashcards.',
                'website': 'https://www.brainscape.com/',
                'features': [
                    ('Deck Builder', 'Create flashcards for high-recall content.', '1. Click Create.\n2. Add cards.\n3. Assign to your class.'),
                    ('Confidence Rating', 'Learners self-rate 1–5.', '1. Review a card.\n2. Rate confidence.\n3. Algorithm resurfaces low-confidence cards.'),
                    ('Class Reports', 'See persistent low-confidence items.', '1. Open Reports.\n2. Sort by confidence.\n3. Plan re-teach.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Gamified Mini-Unit',
                'description': 'Two-lesson gamified sequence with justification memo.',
                'prompt': 'Design a two-lesson gamified mini-unit for a topic you teach. Use at least two tools from this week. In a written memo (min 400 words), justify each mechanic against a specific learning objective — and explain why each one is not just "chocolate-covered broccoli." Submit link to memo and any materials.',
                'submission_type': 'both',
                'rubric': [
                    ('Mechanics-to-objective fit', 'Each mechanic serves a stated objective', 30),
                    ('Tool choice', 'Tools chosen for pedagogical fit, not novelty', 20),
                    ('Reflection quality', 'Acknowledges risks of engagement-without-learning', 25),
                    ('Lesson design', 'Coherent two-lesson sequence', 25),
                ],
            },
        ],
    },
    {
        'number': 8,
        'title': 'Assessment Technology & Learning Analytics',
        'description': 'Google/Microsoft Forms, LMS analytics, digital rubrics.',
        'topics': [
            {
                'title': 'Digital Rubrics',
                'description': 'A scoring guide with named criteria and described performance levels.',
                'materials': [
                    {'title': 'Rubric best practice', 'content': 'Share the rubric with learners before the task, not only at grading time. Use observable, specific language — "good" is not a criterion, "includes three supporting details" is.', 'url': ''},
                ],
            },
        ],
        'tools': [
            {
                'name': 'Google Forms',
                'developer': 'Google',
                'category': 'Assessment',
                'description': 'Auto-graded digital quiz and survey builder.',
                'website': 'https://forms.google.com/',
                'features': [
                    ('Quiz Mode', 'Enable auto-grading.', '1. Open a Form.\n2. Settings > Quizzes > Make this a quiz.\n3. Add answer key to each question.'),
                    ('Instant Feedback', 'Release grades immediately or after review.', '1. Settings > Quizzes.\n2. Choose "Release grade immediately" or "Later, after manual review".'),
                    ('Response Summary', 'See per-question accuracy automatically.', '1. Open the Responses tab.\n2. Click Summary.\n3. Scroll through per-question breakdowns.'),
                ],
            },
            {
                'name': 'Microsoft Forms',
                'developer': 'Microsoft Corporation',
                'category': 'Assessment',
                'description': 'Auto-graded quiz and survey builder within Microsoft 365.',
                'website': 'https://www.microsoft.com/en-us/microsoft-365/online-surveys',
                'features': [
                    ('Quiz Builder', 'Create auto-graded quizzes.', '1. Click New Quiz.\n2. Add questions with correct answers.\n3. Assign points per question.'),
                    ('Teams Embed', 'Embed directly into a Teams class channel.', '1. Open the quiz.\n2. Click Share > Embed in Teams.'),
                    ('Excel Export', 'Export results for further analysis.', '1. Open Responses.\n2. Click Open in Excel.\n3. Analyse in your gradebook.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Data-Informed Re-teach Plan',
                'description': 'A re-teach plan built from a real or simulated class dataset.',
                'prompt': 'Build a 10-question auto-graded quiz on Google Forms or Microsoft Forms. Either run it with your class or simulate results for 20 learners. Then write a 1-paragraph re-teach plan grounded specifically in what the per-question summary shows — identifying the one skill gap and how you will address it. Submit link.',
                'submission_type': 'both',
                'rubric': [
                    ('Quiz construction', '10 clear, well-designed questions', 20),
                    ('Data interpretation', 'Correctly reads per-question data', 30),
                    ('Re-teach specificity', 'Names the exact skill gap and approach', 30),
                    ('Actionability', 'Plan is realistic and specific', 20),
                ],
            },
        ],
    },
    {
        'number': 9,
        'title': 'Inclusive Design, Assistive Technology & Digital Citizenship',
        'description': 'Immersive Reader, Read&Write, digital citizenship.',
        'topics': [
            {
                'title': 'Digital Citizenship Curriculum',
                'description': 'Ready-made lessons on online safety, digital footprint, cyberbullying.',
                'materials': [
                    {'title': 'Common Sense Education Digital Citizenship', 'content': 'Free lesson library. Localize examples with apps learners actually use — not the American defaults.', 'url': 'https://www.commonsense.org/education/digital-citizenship'},
                ],
            },
        ],
        'tools': [
            {
                'name': 'Microsoft Immersive Reader',
                'developer': 'Microsoft Corporation',
                'category': 'Accessibility',
                'description': 'Built-in text-to-speech and reading-support tool.',
                'website': 'https://www.microsoft.com/en-us/education/products/immersive-reader',
                'features': [
                    ('Read Aloud', 'Text-to-speech for any document.', '1. Open a Word doc or Edge-rendered page.\n2. Click the Immersive Reader icon.\n3. Click Read Aloud.'),
                    ('Text Spacing & Font', 'Adjust readability for learners with dyslexia.', '1. In Immersive Reader, open Text Preferences.\n2. Adjust spacing, font, background colour.'),
                    ('Picture Dictionary', 'Define unfamiliar words with a picture.', '1. Click on any word.\n2. Choose Picture Dictionary from the popup.\n3. A picture and definition appear.'),
                ],
            },
            {
                'name': 'Read&Write (Texthelp)',
                'developer': 'Texthelp',
                'category': 'Accessibility',
                'description': 'Literacy support toolbar with text-to-speech, dictionary, translation, word prediction.',
                'website': 'https://www.texthelp.com/products/read-write-education/',
                'features': [
                    ('Read Aloud', 'Text-to-speech on any webpage or Doc.', '1. Install Read&Write extension.\n2. Highlight text.\n3. Click the Read Aloud button.'),
                    ('Word Prediction', 'Suggests words as learners type.', '1. Open Word Prediction.\n2. Begin typing.\n3. Click a prediction to insert.'),
                    ('Translation', 'Support multilingual learners accessing English content.', '1. Highlight text.\n2. Click Translation.\n3. Choose the target language.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Accessibility Audit & Redesign',
                'description': 'Audit one of your existing lesson resources.',
                'prompt': 'Take one reading-heavy resource you already use. Audit it for accessibility: which learners would struggle and why? Redesign it using at least two assistive technology tools from this week. Submit both the original and the redesigned version (links), plus a written audit (min 300 words) covering: (1) barriers identified, (2) tools used, (3) expected impact on specific learner profiles.',
                'submission_type': 'both',
                'rubric': [
                    ('Barrier identification', 'Specific and learner-focused', 25),
                    ('Tool application', 'Two appropriate assistive tools applied well', 30),
                    ('Redesign quality', 'The redesign genuinely removes barriers', 25),
                    ('Written reflection', 'Names specific learner profiles and impacts', 20),
                ],
            },
        ],
    },
    {
        'number': 10,
        'title': 'AI Foundations, Ethics & Data Privacy',
        'description': 'How AI works, hallucination, bias, Kenya Data Protection Act.',
        'topics': [
            {
                'title': 'Generative AI Fundamentals',
                'description': 'AI tools predict plausible output; they do not look up facts.',
                'materials': [
                    {'title': 'Hallucination', 'content': 'Confident, fabricated output presented as fact — a structural feature, not an occasional bug. Always verify AI output against an independent source.', 'url': ''},
                ],
            },
            {
                'title': 'Kenya Data Protection Act 2019',
                'description': 'Applies to any organisation processing personal data of people in Kenya, including schools.',
                'materials': [
                    {'title': 'ODPC — Office of the Data Protection Commissioner', 'content': 'Children\'s data (including academic records) requires heightened protection. Never enter a real learner\'s full name or identifying details into a general-purpose consumer AI tool unless an education-specific data agreement exists.', 'url': 'https://www.odpc.go.ke/'},
                ],
            },
        ],
        'tools': [],
        'assignments': [
            {
                'title': 'Classroom AI-Use Policy',
                'description': 'A one-page policy referencing the Data Protection Act.',
                'prompt': 'Write a one-page AI-use policy for your own classroom or school. Reference the Kenya Data Protection Act 2019 explicitly. Cover: (1) what tools are permitted, (2) what data may never be entered, (3) how academic integrity will be checked, (4) what teachers must review before AI output reaches a learner. Submit a link to the policy document.',
                'submission_type': 'link',
                'rubric': [
                    ('Legal grounding', 'References the DPA and ODPC correctly', 25),
                    ('Data handling rules', 'Clear and specific about what may not be entered', 25),
                    ('Academic integrity', 'Concrete approach, not just a warning', 25),
                    ('Usability', 'A teacher could actually use this policy', 25),
                ],
            },
        ],
    },
    {
        'number': 11,
        'title': 'AI Tools in Practice',
        'description': 'MagicSchool, Diffit, Brisk, Khanmigo, Eduaide, Curipod, NotebookLM, ChatGPT/Claude/Gemini.',
        'topics': [],
        'tools': [
            {
                'name': 'MagicSchool AI',
                'developer': 'MagicSchool AI, Inc.',
                'category': 'AI Tools',
                'description': 'Broad-purpose planning assistant with 80+ generators.',
                'website': 'https://www.magicschool.ai/',
                'features': [
                    ('Lesson Plan Generator', 'First-draft planning.', '1. Select the Lesson Plan tool.\n2. Enter grade, topic, curriculum standard.\n3. Generate, then edit against your goals.'),
                    ('Rubric Generator', 'Draft a starting rubric.', '1. Choose Rubric Generator.\n2. Enter your criteria.\n3. Adjust descriptors to your school\'s language.'),
                    ('IEP Accommodation Writer', 'Suggest accommodations from an input profile.', '1. Open the IEP Accommodation tool.\n2. Describe the learner profile (anonymised).\n3. Review and adapt suggestions.'),
                ],
            },
            {
                'name': 'Diffit',
                'developer': 'Diffit',
                'category': 'AI Tools',
                'description': 'Reading differentiation — adapts any text to multiple reading levels.',
                'website': 'https://web.diffit.me/',
                'features': [
                    ('Multi-level Texts', 'Same content at three or four reading levels.', '1. Paste a passage or topic.\n2. Click Generate.\n3. Choose levels for your class range.'),
                    ('Vocabulary Support', 'Auto-generated vocabulary lists.', '1. After generating text, open the Vocabulary panel.\n2. Review definitions for subject accuracy before sharing.'),
                    ('Comprehension Questions', 'Auto-generated checks per level.', '1. Click Questions.\n2. Select multiple-choice or short answer.\n3. Edit as needed.'),
                ],
            },
            {
                'name': 'Khanmigo',
                'developer': 'Khan Academy',
                'category': 'AI Tools',
                'description': 'Socratic AI tutor — guides with questions, not answers.',
                'website': 'https://www.khanacademy.org/khan-labs',
                'features': [
                    ('Socratic Tutoring', 'Guides learners step-by-step without giving the answer.', '1. Set up a teacher account.\n2. Assign a learner to Khanmigo.\n3. Learners ask questions and are guided by follow-ups.'),
                    ('Teacher-Side Question Generator', 'Draft practice questions aligned to a skill.', '1. Open the teacher dashboard.\n2. Choose a skill.\n3. Generate questions; review before assigning.'),
                    ('Conversation Logs', 'Review learner-AI conversations.', '1. Open Khanmigo reports.\n2. Click a learner.\n3. Read the conversation for quality control.'),
                ],
            },
            {
                'name': 'NotebookLM',
                'developer': 'Google',
                'category': 'AI Tools',
                'description': 'Source-grounded AI notebook — answers only from documents you upload.',
                'website': 'https://notebooklm.google.com/',
                'features': [
                    ('Upload Sources', 'Add PDFs, Docs, slides, or text.', '1. Create a new notebook.\n2. Click Add Source.\n3. Upload your documents.'),
                    ('Grounded Q&A', 'Ask questions; answers cite your sources only.', '1. Type a question in the chat.\n2. Click the citation to see the source passage.'),
                    ('Audio Overview', 'Generate a podcast-style summary.', '1. Click Generate Audio Overview.\n2. Wait for the audio to process.\n3. Share the audio link with learners.'),
                ],
            },
            {
                'name': 'Brisk Teaching',
                'developer': 'Brisk Teaching',
                'category': 'AI Tools',
                'description': 'In-browser AI for feedback and content generation inside Google Docs.',
                'website': 'https://briskteaching.com/',
                'features': [
                    ('Rubric-Aligned Feedback', 'Draft first-pass feedback comments.', '1. Install the Chrome extension.\n2. Open a learner Doc.\n3. Click Brisk > Give Feedback.\n4. Edit every comment before sharing.'),
                    ('Writing Process Replay', 'See revision history to spot AI-generated text.', '1. Open the Doc.\n2. Click Brisk > Writing Process Replay.\n3. Review the paste and typing timeline.'),
                    ('Content Generation', 'Build a worksheet from an existing source.', '1. Open a Doc or Slide.\n2. Click Brisk > Create.\n3. Choose worksheet or quiz.'),
                ],
            },
            {
                'name': 'ChatGPT',
                'developer': 'OpenAI',
                'category': 'AI Tools',
                'description': 'Open-ended conversational AI for brainstorming, drafting, research.',
                'website': 'https://chat.openai.com/',
                'features': [
                    ('Baseline Prompting', 'State role, task, format, and context.', '1. Open a new chat.\n2. Write: "You are a [role]. Help me [task] in [format]. Context: [info]."\n3. Submit.'),
                    ('Step-by-Step Reasoning', 'Ask for step-by-step for complex tasks.', '1. Add "Work step-by-step."\n2. Review the chain of reasoning.'),
                    ('Follow-up Refinement', 'Iterate rather than expecting perfection.', '1. Read the first draft.\n2. Reply with specific edits: "Shorten section 2. Simplify vocabulary."\n3. Review again.'),
                ],
            },
            {
                'name': 'Claude',
                'developer': 'Anthropic',
                'category': 'AI Tools',
                'description': 'Open-ended conversational AI with strong document handling.',
                'website': 'https://claude.ai/',
                'features': [
                    ('Long-Context Documents', 'Upload a syllabus or long reading.', '1. New chat.\n2. Click the attachment icon.\n3. Upload your PDF or Doc.'),
                    ('Projects', 'Persistent custom instructions across chats.', '1. Open Projects.\n2. Add your grade level and curriculum.\n3. Upload reference documents.'),
                    ('Step-by-Step', 'Request chain-of-thought for complex tasks.', '1. Add "Reason step-by-step."\n2. Review reasoning and output.'),
                ],
            },
            {
                'name': 'Gemini',
                'developer': 'Google',
                'category': 'AI Tools',
                'description': 'Google\'s conversational AI, integrated with Workspace.',
                'website': 'https://gemini.google.com/',
                'features': [
                    ('Workspace Integration', 'Draft directly in Docs and Gmail.', '1. Open a Google Doc.\n2. Click Help me write.\n3. Enter a prompt; the draft appears inline.'),
                    ('Multimodal Input', 'Analyse images and documents.', '1. Click the image icon.\n2. Upload a photo or screenshot.\n3. Ask a question about it.'),
                    ('Google It', 'Cross-check Gemini answers against Google Search.', '1. After Gemini responds, click Google It.\n2. Compare sources.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'AI-Assisted Lesson Pack',
                'description': 'A complete lesson pack reviewed and corrected by you.',
                'prompt': 'Use at least three AI tools from this week to build a complete lesson pack: a plan (MagicSchool), differentiated materials (Diffit), and a formative check (any tool). Then write a 300-word reflection documenting every factual or pedagogical correction you made before the pack was ready for learners. Submit the pack link + reflection.',
                'submission_type': 'both',
                'rubric': [
                    ('Tool variety', 'Three appropriate AI tools used', 20),
                    ('Correction documentation', 'Specific corrections with reasoning', 30),
                    ('Pack quality', 'Materials are genuinely usable', 25),
                    ('Reflection depth', 'Shows judgement, not just compliance', 25),
                ],
            },
        ],
    },
    {
        'number': 12,
        'title': 'Blended & Online Pedagogy, and Leadership',
        'description': 'Zoom/Meet/Teams, flipped delivery, ADKAR change management.',
        'topics': [
            {
                'title': 'Change Management — ADKAR',
                'description': 'Awareness, Desire, Knowledge, Ability, Reinforcement.',
                'materials': [
                    {'title': 'Prosci ADKAR Model', 'content': 'Awareness (state the problem), Desire (why adopt), Knowledge (training), Ability (practice + support), Reinforcement (recognise continued use).', 'url': 'https://www.prosci.com/methodology/adkar'},
                ],
            },
        ],
        'tools': [
            {
                'name': 'Zoom',
                'developer': 'Zoom Video Communications',
                'category': 'Communication & Collaboration',
                'description': 'Live video conferencing for synchronous online delivery.',
                'website': 'https://zoom.us/',
                'features': [
                    ('Breakout Rooms', 'Small-group discussion in larger sessions.', '1. Start a meeting.\n2. Click Breakout Rooms.\n3. Choose number of rooms and assignment method.'),
                    ('Live Polls', 'Check understanding mid-session.', '1. In-meeting, click Polls.\n2. Launch a pre-made poll or create one live.\n3. Share results.'),
                    ('Session Recording', 'Capture sessions for absent learners.', '1. Click Record > Record to Cloud.\n2. Get the share link after the meeting ends.'),
                ],
            },
            {
                'name': 'Google Meet',
                'developer': 'Google',
                'category': 'Communication & Collaboration',
                'description': 'Live video conferencing integrated with Google Workspace.',
                'website': 'https://meet.google.com/',
                'features': [
                    ('Meeting Links in Calendar', 'Auto-attach Meet link to calendar invites.', '1. Create a Calendar event.\n2. Click Add Google Meet conferencing.\n3. Invitees join via the event.'),
                    ('Live Captions', 'Real-time captions for accessibility.', '1. In-meeting, click Captions.\n2. Choose language.\n3. Captions appear live.'),
                    ('Recording to Drive', 'Record sessions saved directly to Drive.', '1. Click Activities > Recording.\n2. Click Start Recording.'),
                ],
            },
            {
                'name': 'Microsoft Teams',
                'developer': 'Microsoft',
                'category': 'Communication & Collaboration',
                'description': 'Video conferencing and collaboration hub with class teams.',
                'website': 'https://www.microsoft.com/en-us/microsoft-teams/',
                'features': [
                    ('Class Teams', 'One team per class with channels for topics.', '1. Create a Team.\n2. Choose Class type.\n3. Add learners by email.'),
                    ('Assignments', 'Distribute work with due dates.', '1. In a class team, open Assignments.\n2. Click Create > Assignment.\n3. Set due date.'),
                    ('Breakout Rooms', 'Small-group discussion.', '1. In-meeting, click Breakout Rooms.\n2. Choose number and assign.'),
                ],
            },
        ],
        'assignments': [
            {
                'title': 'Blended Module OR Adoption Proposal',
                'description': 'Either a blended-learning module OR a director-ready adoption proposal.',
                'prompt': 'Choose ONE: (a) Design a blended or flipped lesson module — pre-work, in-class application, debrief — and record a 10-minute walkthrough. OR (b) Draft a one-page ADKAR-structured technology-adoption proposal for a tool from this course, including an agreed review date. Submit the link.',
                'submission_type': 'both',
                'rubric': [
                    ('Choice made and justified', 'Either module or proposal clearly chosen', 20),
                    ('Structure', 'Blended: fits flipped model; Proposal: ADKAR structure complete', 30),
                    ('Realism', 'Practical for a real school context', 25),
                    ('Quality', 'Presentation-ready for its audience', 25),
                ],
            },
        ],
    },
    {
        'number': 13,
        'title': 'Practicum, Peer Critique & Capstone Defense',
        'description': 'Microteaching, peer observation, evaluating EdTech research, capstone portfolio.',
        'topics': [
            {
                'title': 'Structured Peer Observation Protocol',
                'description': 'Observe → score against rubric → compare with self-score → discuss the gap.',
                'materials': [
                    {'title': 'Triple E Framework', 'content': 'Use as part of the shared rubric: SAMR level reached, UDL principles present, engagement evidence.', 'url': 'https://www.tripleeframework.com/'},
                ],
            },
            {
                'title': 'Reading and Evaluating EdTech Research',
                'description': 'Distinguish evidence from enthusiasm.',
                'materials': [
                    {'title': 'EEF Teaching & Learning Toolkit', 'content': 'Summarizes education-intervention research by average impact and evidence strength. Vendor-funded studies require more scrutiny than independently replicated research.', 'url': 'https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit'},
                ],
            },
            {
                'title': 'Capstone Portfolio Assembly',
                'description': 'A unit plan, AI-assisted materials, a taught lesson, and a reflective memo.',
                'materials': [
                    {'title': 'UDL Guidelines (rubric reference)', 'content': 'Portfolio assessed against Bloom\'s, Multiple Intelligences, SAMR, UDL, and Triple E.', 'url': 'https://udlguidelines.cast.org/'},
                ],
            },
        ],
        'tools': [],
        'assignments': [
            {
                'title': 'Capstone Portfolio',
                'description': 'Assemble your full Phase I capstone portfolio.',
                'prompt': 'Assemble a capstone portfolio containing: (1) your backward-designed unit plan, (2) at least one artifact each from Weeks 4, 5, 6, and 7, (3) your AI-assisted lesson pack (Weeks 10–11) with corrections documented, (4) a taught or recorded lesson with peer-observation feedback, (5) a one-page reflective memo connecting your choices back to Bloom\'s, Multiple Intelligences, SAMR, and UDL. Submit a link to the assembled portfolio (Google Drive folder or PDF).',
                'submission_type': 'link',
                'rubric': [
                    ('Completeness', 'All five components present', 20),
                    ('Evidence quality', 'Artifacts are the real, corrected work', 25),
                    ('Reflection memo', 'Frameworks applied to genuine decisions', 30),
                    ('Overall presentation', 'Certification-ready quality', 25),
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the full 13-week curriculum with topics, tools, features, and assignments.'

    def add_arguments(self, parser):
        parser.add_argument('--cohort', type=str, default='September 2026 Cohort')
        parser.add_argument('--reset', action='store_true', help='Delete existing weeks for this cohort before seeding.')

    @transaction.atomic
    def handle(self, *args, **options):
        cohort, _ = Cohort.objects.get_or_create(
            name=options['cohort'],
            defaults={
                'start_date': date(2026, 9, 1),
                'description': 'Full 13-week demo cohort.'
            }
        )
        self.stdout.write(f"Cohort: {cohort.name}")

        if options['reset']:
            self.stdout.write(self.style.WARNING('Deleting existing weeks for this cohort...'))
            Week.objects.filter(cohort=cohort).delete()

        for week_data in WEEKS:
            week, created = Week.objects.get_or_create(
                cohort=cohort, number=week_data['number'],
                defaults={
                    'title': week_data['title'],
                    'description': week_data['description'],
                }
            )
            action = 'Created' if created else 'Found'
            self.stdout.write(f"  {action} Week {week.number}: {week.title}")

            # Topics + materials
            for t_order, topic_data in enumerate(week_data.get('topics', []), start=1):
                topic, _ = Topic.objects.get_or_create(
                    week=week, title=topic_data['title'],
                    defaults={
                        'description': topic_data.get('description', ''),
                        'order': t_order,
                    }
                )
                for m_order, mat in enumerate(topic_data.get('materials', []), start=1):
                    ReferenceMaterial.objects.get_or_create(
                        topic=topic, title=mat['title'],
                        defaults={
                            'content': mat.get('content', ''),
                            'url': mat.get('url', ''),
                            'order': m_order,
                        }
                    )

            # Tools + features
            for tool_order, tool_data in enumerate(week_data.get('tools', []), start=1):
                tool, _ = Tool.objects.get_or_create(
                    week=week, name=tool_data['name'],
                    defaults={
                        'developer': tool_data.get('developer', ''),
                        'category': tool_data.get('category', ''),
                        'description': tool_data.get('description', ''),
                        'website': tool_data.get('website', ''),
                        'order': tool_order,
                    }
                )
                for f_order, (title, purpose, how) in enumerate(tool_data.get('features', []), start=1):
                    ToolFeature.objects.get_or_create(
                        tool=tool, title=title,
                        defaults={
                            'purpose': purpose,
                            'how_to_use': how,
                            'order': f_order,
                        }
                    )

            # Assignments + rubrics
            for a_order, a_data in enumerate(week_data.get('assignments', []), start=1):
                assignment, _ = Assignment.objects.get_or_create(
                    week=week, title=a_data['title'],
                    defaults={
                        'description': a_data.get('description', ''),
                        'prompt': a_data['prompt'],
                        'submission_type': a_data.get('submission_type', 'link'),
                        'is_open_ended': True,
                        'tool': None,
                    }
                )
                for r_order, (name, desc, max_score) in enumerate(a_data.get('rubric', []), start=1):
                    RubricCriterion.objects.get_or_create(
                        assignment=assignment, name=name,
                        defaults={
                            'description': desc,
                            'max_score': max_score,
                            'order': r_order,
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Full curriculum seeded.'))
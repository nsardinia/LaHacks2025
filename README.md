# LaHacks202

## Inspiration
We were inspired to create VibeNotes by imagining our own ideal learning workflow, and how we could leverage AI tools to develop the best possible learning experience for students around the world. 

## What it does

VibeNotes takes and generates pictographic and textual transcriptions from video lecture recordings and handwritten notes to create an in-context AI learning ecosystem powered by knowledge specific to the student's classes, faculty, and academic or professional focus. 

## How we built it

VibeNotes is built as a native Python application using Streamlit for the user interface and data visualization. This approach allowed us to focus on developing high-quality results from our OCR (Paddle) and audio transcription algorithms (OpenAI Whisper). After data is collected and stored in our database (SQLite), we use Google Gemini to determine the best info (video clips, text summaries) to show the student to optimize their understanding of the underlying content. 

## Challenges we ran into

We ran into technical challenges throughout our project development process, especially with managing complex dependencies between different operating systems.

## Accomplishments that we're proud of

Building the CV / OCR / AI Data Pipeline for visual and audio transcription + AI inference over the results was a complicated toolchain to build in such a brief timeframe. 

## What we learned

We practiced our Python skills, learned to develop data-driven applications with Streamlit, explored video recording and streaming over websockets, and used Google Gemini to aggregate and synthesize our results. Additionally, we learned to use OpenAI Whisper to transcribe audio to text, and Paddle OCR to accurately convert handwritten notes to a text format. 

## What's next for VibeNotes

We're looking forward to exploring the potential of AI in education and how we might modify or expand VibeNotes to provide a great service for students everywhere. 



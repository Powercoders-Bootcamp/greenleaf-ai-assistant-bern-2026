from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def export_chunks_to_pdf(chunks, output_path="chunks_output.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()

    story = []

    for chunk in chunks:
        story.append(Paragraph(
            f"<b>Section {chunk.section_number}: {chunk.section_title}</b>",
            styles["Heading2"]
        ))

        story.append(Paragraph(
            f"Chunk index: {chunk.chunk_index} | Words: {chunk.word_count}",
            styles["Normal"]
        ))

        story.append(Spacer(1, 8))

        # escape text for PDF
        text = chunk.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        story.append(Paragraph(text, styles["BodyText"]))

        story.append(Spacer(1, 20))

    doc.build(story)
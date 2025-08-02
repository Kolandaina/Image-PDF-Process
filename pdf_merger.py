from PyPDF2 import PdfMerger

# PDF file paths
pdf_file1 = r'pdf_file1_path.pdf'
pdf_file2 = r'pdf_file2_path.pdf'

output_pdf_path = r'output_path.pdf'

# Create PdfMerger object
merger = PdfMerger()

# Merge PDFs
merger.append(pdf_file1)  # Add first PDF to merger object
merger.append(pdf_file2)  # Add second PDF to merger object

# Save merged PDF
merger.write(output_pdf_path)
merger.close()

print(f"PDF已合并并保存到 {output_pdf_path}")

import fitz  # PyMuPDF
import argparse


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(
        description="Fix margins of PDFs for projection printing")
    parser.add_argument("input", help="Path to the input PDF file")
    parser.add_argument("output", help="Path to save the output PDF file")
    parser.add_argument("-d", "--distance", type=int, default=25,
                        help="Optional: Set the distance of the margin.")

    args = parser.parse_args()

    # Extract the arguments
    input_file = args.input
    output_file = args.output
    distance = args.distance

    pdf = fitz.open(input_file)

    # Define margins to remove (adjust as needed)
    distance = 25
    LEFT = distance   # Points to remove from the left
    TOP = distance    # Points to remove from the top
    RIGHT = distance  # Points to remove from the right
    BOTTOM = distance  # Points to remove from the bottom

    new_pdf = fitz.open()

    # Define the final PDF size (adjust as needed)

    for page in pdf:
        rect = page.rect  # Original page size
        print(rect)
        cropped_rect = fitz.Rect(
            rect.x0 + LEFT,
            rect.y0 + TOP,
            rect.x1 - RIGHT,
            rect.y1 - BOTTOM
        )
        print(cropped_rect)

        # Ensure CropBox is inside MediaBox
        if cropped_rect.x0 < rect.x0 or cropped_rect.y0 < rect.y0 or cropped_rect.x1 > rect.x1 or cropped_rect.y1 > rect.y1:
            print(f"Skipping page {page.number} - CropBox out of bounds")
        else:
            page.set_cropbox(cropped_rect)
            # Force UserUnit to ensure new size is recognized
            page.set_mediabox(cropped_rect)  # Resize page to cropped area
            page.clean_contents()  # Cleanup any cached content data
            page.wrap_contents()  # Ensures page contents fit new dimensions
            # Reset rotation in case it's affecting scaling
            page.set_rotation(0)

            # Manually adjust UserUnit (needed for Adobe Acrobat)

    pdf.save("temp.pdf")
    print(f"Saved cropped PDF as {"temp.pdf"}")
    import os
    os.system(
        f"gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dNoUserUnit -dAutoRotatePages=/None -sOutputFile={output_file} temp.pdf")

    os.remove("temp.pdf")

    # os.system("gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dNoUserUnit -sOutputFile=output.pdf haori-en-mm-cropped.pdf")

    # gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dNoUserUnit -sOutputFile=output.pdf haori-en-mm-cropped.pdf


if __name__ == "__main__":
    main()

import os
import time
import sys
import logging
import shutil
import math
import subprocess
from threading import Thread
from multiprocessing import Value, Lock, Process
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image, ImageOps
import fitz  # PyMuPDF
import colorama
from colorama import Fore, Style
from natsort import natsorted, ns
from pikepdf import Pdf, Rectangle, Name, Stream
import pikepdf

colorama.init()

# New global variables for the new features
remove_first_slides = False
indicate_stars = False
first_slide_numbers = []  # to store the new first slide numbers from each PDF

# Global folders and variables
ORIGIN_FOLDER = 'Input'
RESULT_FOLDER = 'Output'
TEMP_FOLDER = "Temp"
total_page = 0

# Global animation flags
animation_stopped = False               # For merging phase (simple moving box)
animation_stopped2 = False              # For pixel construct: processing slides (image generation)
animation_stopped3 = False              # For pixel construct: drawing slides
animation_stopped_resizing = False      # For vector assembly: resizing animation
animation_stopped_drawing = False       # For vector assembly: drawing animation

# ---------------- Utility Functions ----------------
def check_free_storage():
    """
    Check the free storage on the current drive and return it as a string
    in GB with 2 decimal places.
    """
    total, used, free = shutil.disk_usage(os.getcwd())
    free_gb = free / (1024 ** 3)
    return f"{free_gb:.2f} GB"
    
def remove_previous_logs():
    print(f"{Fore.GREEN}{Style.BRIGHT}Starting new log\n")
    logging.shutdown()
    if os.path.exists('log.txt'):
        os.remove('log.txt')
    logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    print(f"{Fore.GREEN}{Style.BRIGHT}Checking directories...\n")
    for folder in ['Input', 'Output', 'static']:
        if not os.path.exists(folder):
               os.makedirs(folder)

    print("Clearing temp folder\n")
    remove_temp_folder()
    os.makedirs(TEMP_FOLDER, exist_ok=True)

def clear_console():
    if os.name == 'nt':
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear', shell=True)

def remove_temp_folder(max_retries=5, delay=1):
    retries = 0
    while retries < max_retries:
        try:
            if os.path.exists(TEMP_FOLDER):
                shutil.rmtree(TEMP_FOLDER)
            break
        except OSError as e:
            retries += 1
            print(f"Error removing {TEMP_FOLDER}: {e}. Retrying {retries}/{max_retries}...")
            time.sleep(delay)
    else:
        print(f"Failed to remove {TEMP_FOLDER} after {max_retries} retries.")

def unique_filename(base, ext, folder):
    filename = f"{base}{ext}"
    counter = 1
    while os.path.exists(os.path.join(folder, filename)):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename

def format_time(seconds):
    days = int(seconds // 86400)
    seconds %= 86400
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{days}d : {minutes}m : {seconds}s"

# ---------------- Unified Layout Parameters ----------------
def get_layout_params(slide_count_option):
    if slide_count_option == 'A':
        page_size = (595, 842)
        image_height_in = 3.69
        image_width_in = image_height_in * (16/9)
        bottom_margin = 0.311 * inch
        layout_params = {
            'slide_x_position': 1 * inch + (page_size[0] - 2 * inch - image_width_in * inch) / 2,
            'slide_y_positions': [
                page_size[1] - bottom_margin - image_height_in * inch,
                page_size[1] - bottom_margin - 2 * image_height_in * inch,
                page_size[1] - bottom_margin - 3 * image_height_in * inch,
            ],
            'page_size': page_size,
            'image_width': image_width_in * inch,
            'image_height': image_height_in * inch,
            'footer_pos': (7.8 * inch, 0.10 * inch)
        }
        layout_params['orientation'] = 'portrait'
        slides_per_page = 3
        return layout_params, slides_per_page
    else:
        page_size = (11.69 * inch, 8.27 * inch)
        image_width_in = 5.412
        image_height_in = image_width_in * (9/16)
        layout_params = {
            'left_margin': 0.433 * inch,
            'top_margin': 0.7271666667 * inch,
            'row_gap': 0.7271666667 * inch,
            'page_size': page_size,
            'image_width': image_width_in * inch,
            'image_height': image_height_in * inch,
            'footer_pos': (11.2 * inch, 0.307 * inch)
        }
        layout_params['orientation'] = 'landscape'
        slides_per_page = 4
        return layout_params, slides_per_page

# ---------------- Cover Page Parameters & Creation ----------------
cover_params = {
    "A4_portrait": {
        "width": 595,
        "height": 842,
        "title_font": "Times-Bold",
        "title_font_size": 32,
        "title_y": 406.3,
        "cs_line_y": 462,
        "cs_font": "helv",
        "cs_font_size": 20,
        "student_font": "helv",
        "student_font_size": 17,
        "student_y": 802,
        "title_line_thickness": 2,
        "title_line_above_width": 300,
        "title_line_below_width": 481,
        "title_line_above_y": 368,
        "title_line_below_y": 426,
        "backside_text": "Backside of cover",
        "backside_font": "helv",
        "backside_font_size": 12,
        "backside_y": 800
    },
    "A4_landscape": {
        "width": 842,
        "height": 595,
        "title_font": "Times-Bold",
        "title_font_size": 32,
        "title_y": 285.3,
        "cs_line_y": 341,
        "cs_font": "helv",
        "cs_font_size": 20,
        "student_font": "helv",
        "student_font_size": 17,
        "student_y": 555,
        "title_line_thickness": 2,
        "title_line_above_width": 300,
        "title_line_below_width": 481,
        "title_line_above_y": 247,
        "title_line_below_y": 305,
        "backside_text": "Backside of cover",
        "backside_font": "helv",
        "backside_font_size": 12,
        "backside_y": 550
    }
}

def create_cover_page(page_orientation):
    print()
    print(f"{Fore.YELLOW}{Style.BRIGHT}+--------------------------------+\n"
          "|     Details for cover page     |\n"
          "+--------------------------------+")
    try:
        if page_orientation == "Portrait":
            layout = cover_params["A4_portrait"]
        else:
            layout = cover_params["A4_landscape"]

        doc = fitz.open()
        page = doc.new_page(width=layout["width"], height=layout["height"])
        page.draw_rect(fitz.Rect(0, 0, layout["width"], layout["height"]),
                       color=(1, 1, 1), fill=(1, 1, 1))
        while True:
            title_text = input(f"{Fore.YELLOW}{Style.BRIGHT}Title        : ")
            title_font = fitz.Font(layout["title_font"])
            title_width = title_font.text_length(title_text, fontsize=layout["title_font_size"])
            if title_width > 450:
                print(f"{Fore.RED}{Style.BRIGHT}\nInput was too long, consider something shorter.\n")
            else:
                line_above_y = layout["title_line_above_y"]
                line_above_width = layout["title_line_above_width"]
                line_above_start = ((layout["width"] - line_above_width) / 2, line_above_y)
                line_above_end = (((layout["width"] + line_above_width) / 2), line_above_y)
                page.draw_line(line_above_start, line_above_end, color=(0, 0, 0), width=layout["title_line_thickness"])
                title_rect = fitz.Rect(0, layout["title_y"] - layout["title_font_size"],
                                       layout["width"], layout["title_y"] + layout["title_font_size"])
                page.insert_textbox(title_rect, title_text,
                                    fontname=layout["title_font"],
                                    fontsize=layout["title_font_size"],
                                    color=(0, 0, 0),
                                    align=1)
                line_below_y = layout["title_line_below_y"]
                line_below_width = layout["title_line_below_width"]
                line_below_start = ((layout["width"] - line_below_width) / 2, line_below_y)
                line_below_end = (((layout["width"] + line_below_width) / 2), line_below_y)
                page.draw_line(line_below_start, line_below_end, color=(0, 0, 0), width=layout["title_line_thickness"])
                break
        static_chapter = "Chapter: "
        separator = "  |  Subject: "
        cs_font = fitz.Font(layout["cs_font"])
        width_static_chapter = cs_font.text_length(static_chapter, fontsize=layout["cs_font_size"])
        width_separator = cs_font.text_length(separator, fontsize=layout["cs_font_size"])
        max_total_width = 450
        max_user_width = max_total_width - (width_static_chapter + width_separator)
        while True:
            chapter_no = input(f"{Fore.YELLOW}{Style.BRIGHT}Chapter No   : ")
            subject = input(f"{Fore.YELLOW}{Style.BRIGHT}Subject      : ")
            width_chapter_no = cs_font.text_length(chapter_no, fontsize=layout["cs_font_size"])
            width_subject = cs_font.text_length(subject, fontsize=layout["cs_font_size"])
            if width_chapter_no + width_subject > max_user_width:
                print(f"{Fore.RED}{Style.BRIGHT}\nInput was too long. Make the chapter No or subject shorter.\n")
            else:
                cs_text = f"{static_chapter}{chapter_no}{separator}{subject}"
                cs_rect = fitz.Rect(0, layout["cs_line_y"] - layout["cs_font_size"],
                                    layout["width"], layout["cs_line_y"] + layout["cs_font_size"])
                page.insert_textbox(cs_rect, cs_text,
                                    fontname=layout["cs_font"],
                                    fontsize=layout["cs_font_size"],
                                    color=(0, 0, 0),
                                    align=1)
                break
        while True:
            student_name = input(f"{Fore.YELLOW}{Style.BRIGHT}Student Name : ")
            student_font = fitz.Font(layout["student_font"])
            student_width = student_font.text_length(student_name, fontsize=layout["student_font_size"])
            if student_width > 213:
                print(f"{Fore.RED}{Style.BRIGHT}\nInput was too long. Make the student name shorter.\n")
            else:
                bg_padding_top = 1
                bg_padding_bottom = 5.45
                bg_padding_left = 3.8
                bg_padding_right = 4
                margin_left = 60
                margin_right = 60
                student_x_start = layout["width"] - student_width - margin_left - bg_padding_left
                student_x_end = layout["width"] - margin_right + bg_padding_right
                student_y_start = layout["student_y"] - layout["student_font_size"] - bg_padding_top
                student_y_end = layout["student_y"] + bg_padding_bottom
                page.draw_rect(fitz.Rect(student_x_start, student_y_start, student_x_end, student_y_end),
                               color=None, fill=(0, 0, 0))
                page.insert_text((student_x_start + bg_padding_left, layout["student_y"]),
                                 student_name,
                                 fontname=layout["student_font"],
                                 fontsize=layout["student_font_size"],
                                 color=(1, 1, 1))
                break
        doc.new_page(width=layout["width"], height=layout["height"])
        page2 = doc[-1]
        page2.draw_rect(fitz.Rect(0, 0, layout["width"], layout["height"]),
                        color=(1, 1, 1), fill=(1, 1, 1))
        backside_rect = fitz.Rect(
            0,
            layout["backside_y"] - layout["backside_font_size"],
            layout["width"],
            layout["backside_y"] + layout["backside_font_size"]
        )
        page2.insert_textbox(
            backside_rect,
            layout["backside_text"],
            fontname=layout["backside_font"],
            fontsize=layout["backside_font_size"],
            color=(0, 0, 0),
            align=1
        )
        output_path = os.path.join(TEMP_FOLDER, "cover_page.pdf")
        doc.save(output_path)
        doc.close()
    except Exception as e:
        logging.exception("An error occurred while creating the cover page PDF.")
        print("An error occurred while creating the cover page. Please check log.txt for details.")

# ---------------- PDF Merging Functions ----------------
def merge_pdfs_to_result():
    global animation_stopped
    animation_thread = Thread(target=loading_animation)
    animation_thread.start()
    start_time = time.time()
    logging.info("Starting to merge PDFs.")
    files = natsorted([f for f in os.listdir(ORIGIN_FOLDER) if f.endswith('.pdf')], alg=ns.IGNORECASE)
    pdf_count = len(files)
    merged_pdf = fitz.open()
    for file in files:
        file_path = os.path.join(ORIGIN_FOLDER, file)
        with fitz.open(file_path) as pdf:
            merged_pdf.insert_pdf(pdf)
        logging.info(f"Processed file: {file}")
    total_pages = merged_pdf.page_count
    output_filename = unique_filename('Merged_PDF', '.pdf', RESULT_FOLDER)
    result_path = os.path.join(RESULT_FOLDER, output_filename)
    merged_pdf.save(result_path)
    merged_pdf.close()
    logging.info(f"Merged PDF saved to {result_path}")
    animation_stopped = True
    animation_thread.join()
    time_taken = format_time(time.time() - start_time)
    print(f"\n\n{Fore.CYAN}{Style.BRIGHT}File saved to : {Fore.GREEN}{Style.BRIGHT}{result_path}")
    print(f"{Fore.CYAN}{Style.BRIGHT}PDFs Merged   :{Fore.GREEN}{Style.BRIGHT} {pdf_count}")
    print(f"{Fore.CYAN}{Style.BRIGHT}Pages used    :{Fore.GREEN}{Style.BRIGHT} {total_pages}")
    print(f"{Fore.CYAN}{Style.BRIGHT}Time taken    :{Fore.GREEN}{Style.BRIGHT} {time_taken}")
    return result_path

def merge_pdfs_to_temp_pixel():
    global total_page, first_slide_numbers, remove_first_slides
    logging.info("Starting to merge PDFs into temp directory.")
    files = natsorted([f for f in os.listdir(ORIGIN_FOLDER) if f.endswith('.pdf')], alg=ns.IGNORECASE)
    merged_pdf = fitz.open()
    first_slide_numbers = []
    for file in files:
        file_path = os.path.join(ORIGIN_FOLDER, file)
        with fitz.open(file_path) as pdf:
            if remove_first_slides:
                # Always record the marker even for single-page PDFs.
                first_slide_numbers.append(merged_pdf.page_count + 1)
                if pdf.page_count > 1:
                    merged_pdf.insert_pdf(pdf, from_page=1)
                else:
                    logging.info(f"File {file} has only one page; including it and marking for star drawing.")
                    merged_pdf.insert_pdf(pdf)
            else:
                merged_pdf.insert_pdf(pdf)
        logging.info(f"Processed file: {file}")
    temp_filename = 'Merged_PDF_temp.pdf'
    temp_path = os.path.join(TEMP_FOLDER, temp_filename)
    total_page = merged_pdf.page_count
    merged_pdf.save(temp_path)
    merged_pdf.close()
    logging.info(f"Merged PDF saved to {temp_path}")
    return temp_path

def merge_pdfs_to_temp_vector(invert_colors):
    global total_page, first_slide_numbers, remove_first_slides
    logging.info("Starting to merge PDFs into temp directory for vector assembly.")
    files = natsorted([f for f in os.listdir(ORIGIN_FOLDER) if f.lower().endswith('.pdf')], alg=ns.IGNORECASE)
    merged_pdf = fitz.open()
    first_slide_numbers = []
    for file in files:
        file_path = os.path.join(ORIGIN_FOLDER, file)
        with fitz.open(file_path) as pdf:
            if remove_first_slides:
                # Always record the marker even for single-page PDFs.
                first_slide_numbers.append(merged_pdf.page_count + 1)
                if pdf.page_count > 1:
                    merged_pdf.insert_pdf(pdf, from_page=1)
                else:
                    logging.info(f"File {file} has only one page; including it and marking for star drawing.")
                    merged_pdf.insert_pdf(pdf)
            else:
                merged_pdf.insert_pdf(pdf)
        logging.info(f"Processed file: {file}")
    temp_filename = 'Merged_PDF_temp.pdf'
    temp_path = os.path.join(TEMP_FOLDER, temp_filename)
    total_page = merged_pdf.page_count
    merged_pdf.save(temp_path)
    merged_pdf.close()
    logging.info(f"Merged PDF saved to {temp_path}")
    if invert_colors:
        logging.info("Inverting colors of the merged PDF using vector assembly method.")
        try:
            with pikepdf.open(temp_path, allow_overwriting_input=True) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    try:
                        media_box = page.MediaBox
                        width = float(media_box[2]) - float(media_box[0])
                        height = float(media_box[3]) - float(media_box[1])
                        if "/Resources" not in page:
                            page["/Resources"] = pikepdf.Dictionary()
                        resources = page["/Resources"]
                        if "/ExtGState" not in resources:
                            resources["/ExtGState"] = pikepdf.Dictionary()
                        extgstate = resources["/ExtGState"]
                        extgstate["/InvertGS"] = pikepdf.Dictionary({
                            "/BM": pikepdf.Name("/Difference")
                        })
                        bg_stream_content = (
                            "q\n"
                            "1 1 1 rg\n"
                            f"0 0 {width} {height} re\n"
                            "f\n"
                            "Q\n"
                        )
                        bg_bytes = bg_stream_content.encode('utf-8')
                        bg_stream = pikepdf.Stream(pdf, bg_bytes)
                        inversion_stream_content = (
                            "q\n"
                            "/InvertGS gs\n"
                            "1 1 1 rg\n"
                            f"0 0 {width} {height} re\n"
                            "f\n"
                            "Q\n"
                        )
                        inv_bytes = inversion_stream_content.encode('utf-8')
                        inversion_stream = pikepdf.Stream(pdf, inv_bytes)
                        orig_contents = page.Contents
                        if isinstance(orig_contents, pikepdf.Array):
                            new_contents = pikepdf.Array([bg_stream] + list(orig_contents) + [inversion_stream])
                        else:
                            new_contents = pikepdf.Array([bg_stream, orig_contents, inversion_stream])
                        page.Contents = new_contents
                    except Exception as page_err:
                        logging.error(f"Error processing page {page_num}: {page_err}")
                pdf.save(temp_path)
            logging.info(f"Inverted PDF saved to: {temp_path}")
        except Exception as e:
            logging.error(f"Failed to invert colors in vector assembly mode: {e}")
    return temp_path

# ---------------- Function to Add Star Symbols ----------------
def add_star_symbols(output_path, slides_per_page):
    # Star layouts for 3 and 4 slides per page
    STAR_LAYOUTS = {
        "3": [
            (540, 73.5),
            (540, 339.2),
            (540, 604.7)
        ],
        "4": [
            (50, 67),
            (440, 67),
            (50, 338.7),
            (440, 338.7)
        ]
    }
    print(f"{Fore.YELLOW}{Style.BRIGHT}\nAdding indicator symbols...")
    doc = fitz.open(output_path)
    # Use the full list now so the last pdf's first slide is not ignored.
    star_list = first_slide_numbers
    for slide_number in star_list:
        merged_page_number = math.ceil(slide_number / slides_per_page)
        position = ((slide_number - 1) % slides_per_page) + 1
        if str(slides_per_page) in STAR_LAYOUTS and (position - 1) < len(STAR_LAYOUTS[str(slides_per_page)]):
            x, y = STAR_LAYOUTS[str(slides_per_page)][position - 1]
            page_index = merged_page_number - 1  # fitz pages are 0-indexed
            if page_index < doc.page_count:
                page = doc[page_index]
                page.insert_text((x, y), "*", fontname="helv", fontsize=50, color=(0, 0, 0))
                logging.info(f"Added star on page {merged_page_number} at position {position}")
            else:
                logging.warning(f"Calculated page index {page_index} out of range for stars.")
        else:
            logging.warning("Star layout not defined for slides per page: " + str(slides_per_page))
    doc.saveIncr()
    doc.close()

# ---------------- Pixel Construct Functions ----------------
def generate_images(page_range, merged_pdf_path, dpi, invert_colors, image_width_in, image_height_in):
    target_width = image_width_in * dpi
    target_height = image_height_in * dpi
    with fitz.open(merged_pdf_path) as pdf_document:
        for page_num in page_range:
            page = pdf_document.load_page(page_num)
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height
            page_ratio = page_width / page_height
            target_ratio = 16 / 9
            if page_ratio > target_ratio:
                matrix_value = target_height / page_height
            else:
                matrix_value = target_width / page_width
            matrix = fitz.Matrix(matrix_value, matrix_value)
            pix = page.get_pixmap(matrix=matrix)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            original_width, original_height = img.size
            aspect_ratio = 16 / 9
            image_ratio = original_width / original_height
            if abs(image_ratio - aspect_ratio) > 0.01:
                scaling_factor = min(original_width / 16, original_height / 9)
                target_w = int(16 * scaling_factor)
                target_h = int(9 * scaling_factor)
                img = img.resize((target_w, target_h), Image.LANCZOS)
            if invert_colors:
                img = ImageOps.invert(img)
            temp_image_path = os.path.join(TEMP_FOLDER, f"temp_slide_{page_num}.png")
            img.save(temp_image_path)

def draw_slides_pages_worker(start_page, end_page, slides_per_page, layout_params, total_images, temp_folder, output_pdf_path, processed_pages_ref, processed_pages_lock):
    c = canvas.Canvas(output_pdf_path, pagesize=layout_params['page_size'])
    page_number = start_page
    for page in range(start_page, end_page + 1):
        for slide_index in range(slides_per_page):
            global_image_index = (page - 1) * slides_per_page + slide_index
            if global_image_index < total_images:
                image_path = os.path.join(temp_folder, f"temp_slide_{global_image_index}.png")
                if 'slide_y_positions' in layout_params:
                    x_pos = layout_params['slide_x_position']
                    y_pos = layout_params['slide_y_positions'][slide_index]
                else:
                    row = slide_index // 2
                    col = slide_index % 2
                    x_pos = layout_params['left_margin'] + col * layout_params['image_width']
                    y_pos = layout_params['page_size'][1] - layout_params['top_margin'] - layout_params['image_height'] - row * (layout_params['image_height'] + layout_params['row_gap'])
                c.drawImage(image_path, x_pos, y_pos, width=layout_params['image_width'], height=layout_params['image_height'], preserveAspectRatio=True)
                c.rect(x_pos, y_pos, layout_params['image_width'], layout_params['image_height'])
        c.setFont("Helvetica", 10)
        c.drawRightString(*layout_params['footer_pos'], f"{page_number}")
        c.showPage()
        with processed_pages_lock:
            processed_pages_ref.value += 1
        page_number += 1
    c.save()

# ---------------- Updated Summary Function ----------------
def show_merge_summary(slide_count, pages_used, output_path, pdf_count=None, total_time=None):
    shutil.rmtree(TEMP_FOLDER, ignore_errors=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    print()
    print(f"{Fore.CYAN}{Style.BRIGHT}File saved to :{Fore.GREEN}{Style.BRIGHT} {output_path}")
    if pdf_count is not None:
         print(f"{Fore.CYAN}{Style.BRIGHT}PDFs Merged   :{Fore.GREEN}{Style.BRIGHT} {pdf_count}")
    print(f"{Fore.CYAN}{Style.BRIGHT}Slides merged :{Fore.GREEN}{Style.BRIGHT} {slide_count}")
    print(f"{Fore.CYAN}{Style.BRIGHT}Pages used    :{Fore.GREEN}{Style.BRIGHT} {pages_used}")
    if total_time is not None:
         print(f"{Fore.CYAN}{Style.BRIGHT}Time taken    :{Fore.GREEN}{Style.BRIGHT} {total_time}")
    logging.info(f"Slides merged: {slide_count}")
    logging.info(f"Pages used: {pages_used}")

def loading_animation():
    global animation_stopped
    box_width = 3
    filled_box = "■"
    empty_box = " "
    left_to_right = True
    position = 0
    while not animation_stopped:
        loading_box = empty_box * position + filled_box + empty_box * (box_width - position - 1)
        sys.stdout.write(f"\r{Fore.WHITE}{Style.BRIGHT}[{loading_box}]")
        sys.stdout.flush()
        time.sleep(0.1)
        if left_to_right:
            position += 1
            if position == box_width - 1:
                left_to_right = False
        else:
            position -= 1
            if position == 0:
                left_to_right = True

def loading_animation2():
    global animation_stopped2, total_page
    box_width = 20
    filled_char = "■"
    empty_char = "-"
    start_time = time.time()
    try:
        while not animation_stopped2:
            total_file = len([f for f in os.listdir(TEMP_FOLDER) if f != "Merged_PDF_temp.pdf" and os.path.isfile(os.path.join(TEMP_FOLDER, f))])
            if total_page > 0:
                percentage = (total_file / total_page) * 100
            else:
                percentage = 100
            percentage = min(max(percentage, 0), 100)
            filled_segments = int((percentage / 100) * box_width)
            elapsed_time = time.time() - start_time
            if total_file > 0:
                avg_time_per_percent = elapsed_time / total_file
            else:
                avg_time_per_percent = 0
            remaining_time = max(0, total_page - total_file) * avg_time_per_percent
            remaining_minutes = int(remaining_time // 60)
            remaining_seconds = int(remaining_time % 60)
            progress_bar = f"[{filled_char * filled_segments}{empty_char * (box_width - filled_segments)}]"
            sys.stdout.write(f"\r{Fore.CYAN}{Style.BRIGHT}{progress_bar} | {percentage:.2f}% | ETA {remaining_minutes:02}:{remaining_seconds:02}")
            sys.stdout.flush()
            time.sleep(0.1)
    except Exception as e:
        logging.error(f"Error in loading animation2: {e}")

def loading_animation3(processed_pages_ref, total_pages, processed_pages_lock):
    global animation_stopped3
    box_width = 20
    filled_char = "■"
    empty_char = "-"
    start_time = time.time()
    try:
        while not animation_stopped3:
            with processed_pages_lock:
                processed_pages = processed_pages_ref.value
            if total_pages > 0:
                percentage = (processed_pages / total_pages) * 100
            else:
                percentage = 100
            percentage = min(max(percentage, 0), 100)
            filled_segments = int((percentage / 100) * box_width)
            elapsed_time = time.time() - start_time
            if processed_pages > 0:
                avg_time_per_page = elapsed_time / processed_pages
            else:
                avg_time_per_page = 0
            remaining_time = (total_pages - processed_pages) * avg_time_per_page
            remaining_minutes = int(remaining_time // 60)
            remaining_seconds = int(remaining_time % 60)
            progress_bar = f"[{filled_char * filled_segments}{empty_char * (box_width - filled_segments)}]"
            sys.stdout.write(f"\r{Fore.GREEN}{Style.BRIGHT}{progress_bar} | {percentage:.2f}% | ETA {remaining_minutes:02}:{remaining_seconds:02}")
            sys.stdout.flush()
            time.sleep(0.1)
    except Exception as e:
        logging.error(f"Error in loading animation3: {e}")

# ---------------- Vector Assembly Functions ----------------
def calculate_16_9_dimensions(width, height):
    target_ratio = 16 / 9
    page_ratio = width / height
    if page_ratio > target_ratio:
        new_width = height * target_ratio
        new_height = height
    else:
        new_width = width
        new_height = width / target_ratio
    return new_width, new_height

def process_resize_range(input_pdf_path, start_page, end_page, output_path, processed_pages_ref, processed_pages_lock):
    try:
        doc_in = fitz.open(input_pdf_path)
        doc_out = fitz.open()
        for page_num in range(start_page, end_page + 1):
            page = doc_in[page_num]
            media_box = page.mediabox
            new_width, new_height = calculate_16_9_dimensions(media_box.width, media_box.height)
            new_page = doc_out.new_page(-1, width=new_width, height=new_height)
            new_page.show_pdf_page(new_page.rect, doc_in, page_num, keep_proportion=False)
            with processed_pages_lock:
                processed_pages_ref.value += 1
        doc_in.close()
        doc_out.save(output_path)
        doc_out.close()
    except Exception as e:
        logging.error(f"Error in process_resize_range for pages {start_page}-{end_page}: {e}")

def resizing_animation(processed_pages_ref, total_pages, processed_pages_lock):
    global animation_stopped_resizing
    box_width = 20
    filled_char = "■"
    empty_char = "-"
    start_time = time.time()
    try:
        while not animation_stopped_resizing:
            with processed_pages_lock:
                processed_pages = processed_pages_ref.value
            percentage = (processed_pages / total_pages) * 100 if total_pages > 0 else 100
            percentage = min(max(percentage, 0), 100)
            filled_segments = int((percentage / 100) * box_width)
            elapsed_time = time.time() - start_time
            avg_time = elapsed_time / processed_pages if processed_pages > 0 else 0
            remaining_time = (total_pages - processed_pages) * avg_time
            remaining_minutes = int(remaining_time // 60)
            remaining_seconds = int(remaining_time % 60)
            progress_bar = f"[{filled_char * filled_segments}{empty_char * (box_width - filled_segments)}]"
            sys.stdout.write(f"\r{Fore.CYAN}{Style.BRIGHT}{progress_bar} | {percentage:.2f}% | ETA {remaining_minutes:02}:{remaining_seconds:02}")
            sys.stdout.flush()
            time.sleep(0.1)
    except Exception as e:
        logging.error(f"Error in resizing animation: {e}")

def drawing_animation(processed_pages_ref, total_pages, processed_pages_lock):
    global animation_stopped_drawing
    box_width = 20
    filled_char = "■"
    empty_char = "-"
    start_time = time.time()
    try:
        while not animation_stopped_drawing:
            with processed_pages_lock:
                processed_pages = processed_pages_ref.value
            percentage = (processed_pages / total_pages) * 100 if total_pages > 0 else 100
            percentage = min(max(percentage, 0), 100)
            filled_segments = int((percentage / 100) * box_width)
            elapsed_time = time.time() - start_time
            avg_time = elapsed_time / processed_pages if processed_pages > 0 else 0
            remaining_time = (total_pages - processed_pages) * avg_time
            remaining_minutes = int(remaining_time // 60)
            remaining_seconds = int(remaining_time % 60)
            progress_bar = f"[{filled_char * filled_segments}{empty_char * (box_width - filled_segments)}]"
            sys.stdout.write(f"\r{Fore.GREEN}{Style.BRIGHT}{progress_bar} | {percentage:.2f}% | ETA {remaining_minutes:02}:{remaining_seconds:02}")
            sys.stdout.flush()
            time.sleep(0.1)
    except Exception as e:
        logging.error(f"Error in drawing animation: {e}")

def resize_merged_pdf_to_16_9(temp_path):
    doc = fitz.open(temp_path)
    total_pages = len(doc)
    doc.close()
    global animation_stopped_resizing
    if total_pages < 5:
        print(f"\n\n{Fore.YELLOW}{Style.BRIGHT}Resizing slides (SP)...")
        processed_pages_ref = Value('i', 0)
        processed_pages_lock = Lock()
        animation_stopped_resizing = False
        progress_thread = Thread(target=resizing_animation, args=(processed_pages_ref, total_pages, processed_pages_lock))
        progress_thread.start()
        doc_in = fitz.open(temp_path)
        doc_out = fitz.open()
        for page_num in range(total_pages):
            page = doc_in[page_num]
            media_box = page.mediabox
            new_width, new_height = calculate_16_9_dimensions(media_box.width, media_box.height)
            new_page = doc_out.new_page(-1, width=new_width, height=new_height)
            new_page.show_pdf_page(new_page.rect, doc_in, page_num, keep_proportion=False)
            with processed_pages_lock:
                processed_pages_ref.value += 1
        time.sleep(0.1)
        animation_stopped_resizing = True
        progress_thread.join()
        print(f"\n\n{Fore.YELLOW}{Style.BRIGHT}Saving resized PDF...")
        resized_temp_path = temp_path.replace(".pdf", "_resized.pdf")
        doc_out.save(resized_temp_path)
        doc_in.close()
        doc_out.close()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\nCleaning up...")
        os.remove(temp_path)
        os.rename(resized_temp_path, temp_path)
        logging.info(f"Resized merged PDF pages to 16:9 ratio and saved to {temp_path}")
    else:
        print(f"\n\n{Fore.YELLOW}{Style.BRIGHT}Resizing slides (MP)...")
        pages_per_process = total_pages // 5
        remainder = total_pages % 5
        processes = []
        output_files = []
        processed_pages_ref = Value('i', 0)
        processed_pages_lock = Lock()
        animation_stopped_resizing = False
        progress_thread = Thread(target=resizing_animation, args=(processed_pages_ref, total_pages, processed_pages_lock))
        progress_thread.start()
        current_start = 0
        for i in range(5):
            if pages_per_process > 0:
                start = current_start
                end = start + pages_per_process - 1
                output_file = os.path.join(TEMP_FOLDER, f"{i+1}_resized.pdf")
                p = Process(target=process_resize_range, args=(temp_path, start, end, output_file, processed_pages_ref, processed_pages_lock))
                processes.append(p)
                output_files.append(output_file)
                current_start += pages_per_process
            else:
                break
        if remainder > 0:
            start = current_start
            end = total_pages - 1
            output_file = os.path.join(TEMP_FOLDER, f"{len(processes)+1}_resized.pdf")
            p = Process(target=process_resize_range, args=(temp_path, start, end, output_file, processed_pages_ref, processed_pages_lock))
            processes.append(p)
            output_files.append(output_file)
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        time.sleep(0.1)
        animation_stopped_resizing = True
        progress_thread.join()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\n\nCleaning up...")
        if os.path.exists(temp_path):  
            try:  
                os.remove(temp_path)  
                logging.info(f"Deleted temporary file: {temp_path}")  
            except Exception as e:  
                logging.warning(f"Could not delete {temp_path}: {e}")  
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Saving resized PDF...")
        merged_doc = fitz.open()
        sorted_files = natsorted(output_files, alg=ns.IGNORECASE)
        for file in sorted_files:
            with fitz.open(file) as part_pdf:
                merged_doc.insert_pdf(part_pdf)
        merged_resized_path = temp_path.replace(".pdf", "_resized.pdf")
        merged_doc.save(merged_resized_path)
        merged_doc.close()
        os.rename(merged_resized_path, temp_path)
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\nCleaning up...")
        for file in output_files:
            try:
                os.remove(file)
            except Exception as e:
                logging.warning(f"Could not remove temporary file {file}: {e}")
        logging.info(f"Resized merged PDF pages using multiprocessing to 16:9 ratio and saved to {temp_path}")

# ---------------- Updated process_page_range_vector ----------------
def process_page_range_vector(start_page, end_page, merged_pdf_path, layout, output_path, start_footer, processed_pages_ref, processed_pages_lock):
    try:
        with Pdf.open(merged_pdf_path) as pdf:
            num_slides = len(pdf.pages)
            output_pdf = Pdf.new()
            slides_per_page = layout.get('slides_per_page', 0)
            for output_page_num in range(start_page, end_page + 1):
                output_page = output_pdf.add_blank_page(page_size=layout['page_size'])
                border_positions = []
                for j in range(slides_per_page):
                    slide_index = output_page_num * slides_per_page + j
                    if slide_index >= num_slides:
                        break
                    if layout.get('orientation', '') == 'portrait':
                        x = layout['slide_x_position']
                        if j < len(layout['slide_y_positions']):
                            y = layout['slide_y_positions'][j] + layout['image_height']
                        else:
                            y = layout['slide_y_positions'][-1] + layout['image_height']
                    else:
                        row = j // 2
                        col = j % 2
                        x = layout['left_margin'] + col * layout['image_width']
                        y = layout['page_size'][1] - layout['top_margin'] - row * (layout['image_height'] + layout['row_gap'])
                    dest_rect = Rectangle(x, y - layout['image_height'], x + layout['image_width'], y)
                    slide = pdf.pages[slide_index]
                    output_page.add_overlay(slide, dest_rect)
                    border_positions.append((x, y, layout['image_width'], layout['image_height']))
                content_parts = []
                for (x_pos, y_pos, w, h) in border_positions:
                    border_commands = [
                        "q",
                        f"{layout.get('border_thickness', 1)} w",
                        f"{x_pos} {y_pos} m",
                        f"{x_pos + w} {y_pos} l",
                        f"{x_pos + w} {y_pos - h} l",
                        f"{x_pos} {y_pos - h} l",
                        "h",
                        "S",
                        "Q"
                    ]
                    content_parts.append("\n".join(border_commands))
                footer_x, footer_y = layout['footer_pos']
                text = str(start_footer + (output_page_num - start_page))
                text_width = len(text) * 5
                adjusted_x = footer_x - text_width
                footer_commands = [
                    "BT",
                    "/Helvetica 10 Tf",
                    f"{adjusted_x} {footer_y} Td",
                    f"({text}) Tj",
                    "ET"
                ]
                content_parts.append("\n".join(footer_commands))
                overlay_stream = "\n".join(content_parts).encode()
                if Name.Contents in output_page:
                    existing = output_page[Name.Contents].read_bytes()
                    combined = existing + b"\n" + overlay_stream
                else:
                    combined = overlay_stream
                output_page[Name.Contents] = Stream(output_pdf, combined)
                with processed_pages_lock:
                    processed_pages_ref.value += 1
        output_pdf.save(output_path)
    except Exception as e:
        logging.error(f"Error processing pages {start_page}-{end_page}: {e}")

# ---------------- Vector Assembly Slides Merger ----------------
def vector_assembly_slides_merger(slide_count_option, invert_colors, cover_merge):
    global animation_stopped, animation_stopped_drawing, total_page
    output_filename = unique_filename('Merged_slides', '.pdf', RESULT_FOLDER)
    output_path = os.path.join(RESULT_FOLDER, output_filename)
    layout, slides_per_page = get_layout_params(slide_count_option)
    layout['slides_per_page'] = slides_per_page
    start_time = time.time()
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Merging PDFs to temp directory...")
    pdf_files = natsorted([f for f in os.listdir(ORIGIN_FOLDER) if f.lower().endswith('.pdf')], alg=ns.IGNORECASE)
    pdf_count = len(pdf_files)
    animation_thread = Thread(target=loading_animation)
    animation_thread.start()
    try:
        merged_pdf_path = merge_pdfs_to_temp_vector(invert_colors)
    except Exception as e:
        animation_stopped = True
        print(f"{Fore.RED}{Style.BRIGHT}An error occurred while merging PDFs: {e}")
        logging.error(f"Error merging PDFs: {e}")
        return
    animation_stopped = True
    animation_thread.join()
    resize_merged_pdf_to_16_9(merged_pdf_path)
    num_slides = total_page
    required_pages = math.ceil(num_slides / layout['slides_per_page'])
    processed_pages_ref = Value('i', 0)
    processed_pages_lock = Lock()
    if required_pages < 4:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Drawing slides (SP)...")
        animation_stopped_drawing = False
        drawing_thread = Thread(target=drawing_animation, args=(processed_pages_ref, required_pages, processed_pages_lock))
        drawing_thread.start()
        process_page_range_vector(0, required_pages - 1, merged_pdf_path, layout, output_path, 1, processed_pages_ref, processed_pages_lock)
        time.sleep(0.1)
        animation_stopped_drawing = True
        drawing_thread.join()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\n\nCleaning up...")
        try:
            if os.path.exists(merged_pdf_path):
                os.remove(merged_pdf_path)
                logging.info(f"Deleted temporary resized PDF: {merged_pdf_path}")
        except Exception as e:
            logging.error(f"Failed to delete {merged_pdf_path}: {e}")
    else:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Drawing slides (MP)...")
        animation_stopped_drawing = False
        drawing_thread = Thread(target=drawing_animation, args=(processed_pages_ref, required_pages, processed_pages_lock))
        drawing_thread.start()
        processes = []
        output_parts = []
        pages_per_process = required_pages // 5
        remainder = required_pages % 5
        current_start = 0
        start_footer = 1
        for i in range(5):
            if pages_per_process > 0:
                start = current_start
                end = current_start + pages_per_process - 1
                part_path = os.path.join(TEMP_FOLDER, f"part_{i}.pdf")
                p = Process(target=process_page_range_vector, args=(start, end, merged_pdf_path, layout, part_path, start_footer, processed_pages_ref, processed_pages_lock))
                processes.append(p)
                output_parts.append(part_path)
                current_start += pages_per_process
                start_footer += pages_per_process
            else:
                break
        if remainder > 0:
            part_path = os.path.join(TEMP_FOLDER, f"part_{len(processes)}.pdf")
            p = Process(target=process_page_range_vector, args=(current_start, required_pages - 1, merged_pdf_path, layout, part_path, start_footer, processed_pages_ref, processed_pages_lock))
            processes.append(p)
            output_parts.append(part_path)
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        time.sleep(0.1)
        animation_stopped_drawing = True
        drawing_thread.join()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\n\nCleaning up...")
        try:
            if os.path.exists(merged_pdf_path):
                os.remove(merged_pdf_path)
                logging.info(f"Deleted temporary resized PDF: {merged_pdf_path}")
        except Exception as e:
            logging.error(f"Failed to delete {merged_pdf_path}: {e}")
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Saving final PDF...")
        final_pdf = fitz.open()
        for part in natsorted(output_parts, alg=ns.IGNORECASE):
            with fitz.open(part) as part_pdf:
                final_pdf.insert_pdf(part_pdf)
        final_pdf.save(output_path)
        final_pdf.close()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\nCleaning up...")
        for part in output_parts:
            try:
                os.remove(part)
            except Exception as e:
                logging.warning(f"Could not remove temporary file {part}: {e}")
    # Add star symbols now (if removal & indication selected) just before cover merge
    if remove_first_slides and indicate_stars:
        add_star_symbols(output_path, slides_per_page)
    if cover_merge:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Inserting cover page...")
        cover_pdf_path = os.path.join(TEMP_FOLDER, "cover_page.pdf")
        if os.path.exists(cover_pdf_path):
            cover_pdf = fitz.open(cover_pdf_path)
            cover_page_count = cover_pdf.page_count
            final_pdf = fitz.open(output_path)
            final_pdf.insert_pdf(cover_pdf, from_page=0, to_page=cover_page_count - 1, start_at=0)
            final_pdf.set_page_labels([])
            final_pdf.saveIncr()
            final_pdf.close()
            cover_pdf.close()
            logging.info("Cover page added successfully.")
            final_page_count = required_pages + cover_page_count
        else:
            final_page_count = required_pages
    else:
        final_page_count = required_pages
    total_time = format_time(time.time() - start_time)
    show_merge_summary(num_slides, final_page_count, output_path, pdf_count, total_time)
    return output_path

# ---------------- Pixel Construct Slides Merger (Original) ----------------
def acs_class_slides_merger(slide_count_option, dpi, invert_colors, cover_merge=False):
    global animation_stopped, animation_stopped2, animation_stopped3
    output_filename = unique_filename('Merged_slides', '.pdf', RESULT_FOLDER)
    output_path = os.path.join(RESULT_FOLDER, output_filename)
    layout_params, slides_per_page = get_layout_params(slide_count_option)
    layout_params['slides_per_page'] = slides_per_page
    start_time = time.time()
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Merging PDFs to temp directory...")
    pdf_files = natsorted([f for f in os.listdir(ORIGIN_FOLDER) if f.endswith('.pdf')], alg=ns.IGNORECASE)
    pdf_count = len(pdf_files)
    animation_thread = Thread(target=loading_animation)
    animation_thread.start()
    try:
        merged_pdf_path = merge_pdfs_to_temp_pixel()
    except Exception as e:
        animation_stopped = True
        animation_thread.join()
        print(f"{Fore.RED}{Style.BRIGHT}An error occurred while merging PDFs: {e}")
        logging.error(f"Error merging PDFs: {e}")
        return
    animation_stopped = True
    animation_thread.join()
    animation_thread2 = Thread(target=loading_animation2)
    animation_thread2.start()
    try:
        if total_page < 5:
            print(f"\n\n{Fore.YELLOW}{Style.BRIGHT}Processing slides (SP)...")
            generate_images(range(total_page), merged_pdf_path, dpi, invert_colors, layout_params['image_width']/inch, layout_params['image_height']/inch)
        else:
            print(f"\n\n{Fore.YELLOW}{Style.BRIGHT}Processing slides (MP)...")
            processes = []
            pages_per_process = total_page // 5
            remainder = total_page % 5
            for i in range(5):
                start = i * pages_per_process
                end = start + pages_per_process
                if i == 4:
                    end += remainder
                page_range = range(start, end)
                p = Process(target=generate_images, args=(page_range, merged_pdf_path, dpi, invert_colors, layout_params['image_width']/inch, layout_params['image_height']/inch))
                processes.append(p)
                p.start()
            for p in processes:
                p.join()
                if p.exitcode != 0:
                    logging.error(f"Process {p.pid} exited with code {p.exitcode}")
                    print(f"{Fore.RED}{Style.BRIGHT}An error occurred in one of the processes (PID: {p.pid}). Check logs for details.")
                    return
        time.sleep(0.1)
        animation_stopped2 = True
        animation_thread2.join()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\n\nCleaning up...")
        if os.path.exists(merged_pdf_path):
            try:
                os.remove(merged_pdf_path)
                logging.info(f"Deleted temporary merged PDF: {merged_pdf_path}")
            except Exception as e:
                logging.error(f"Failed to delete {merged_pdf_path}: {e}")
        image_files = natsorted([f for f in os.listdir(TEMP_FOLDER) if f.startswith('temp_slide_') and f.endswith('.png')], alg=ns.IGNORECASE)
        total_images = len(image_files)
        total_pages = (total_images + slides_per_page - 1) // slides_per_page
        processed_pages_ref = Value('i', 0)
        processed_pages_lock = Lock()
        animation_stopped3 = False
        if total_images < 4 * slides_per_page:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Drawing slides (SP)...")
            animation_thread3 = Thread(target=loading_animation3, args=(processed_pages_ref, total_pages, processed_pages_lock))
            animation_thread3.start()
            c = canvas.Canvas(output_path, pagesize=layout_params['page_size'])
            page_count = 1
            for page_index in range(total_pages):
                for slide_index in range(slides_per_page):
                    global_index = page_index * slides_per_page + slide_index
                    if global_index < total_images:
                        temp_image_path = os.path.join(TEMP_FOLDER, f"temp_slide_{global_index}.png")
                        if 'slide_y_positions' in layout_params:
                            x_pos = layout_params['slide_x_position']
                            y_pos = layout_params['slide_y_positions'][slide_index]
                        else:
                            row = slide_index // 2
                            col = slide_index % 2
                            x_pos = layout_params['left_margin'] + col * layout_params['image_width']
                            y_pos = layout_params['page_size'][1] - layout_params['top_margin'] - layout_params['image_height'] - row * (layout_params['image_height'] + layout_params['row_gap'])
                        c.drawImage(temp_image_path, x_pos, y_pos,
                                    width=layout_params['image_width'],
                                    height=layout_params['image_height'],
                                    preserveAspectRatio=True)
                        c.rect(x_pos, y_pos, layout_params['image_width'], layout_params['image_height'])
                c.setFont("Helvetica", 10)
                c.drawRightString(*layout_params['footer_pos'], f"{page_count}")
                c.showPage()
                with processed_pages_lock:
                    processed_pages_ref.value += 1
                page_count += 1
            c.save()
            logging.info("Drawing slides completed")
            time.sleep(0.1)
            animation_stopped3 = True
            animation_thread3.join()
            print(f"{Fore.MAGENTA}{Style.BRIGHT}\n\nCleaning up...")
            for file in os.listdir("Temp"):
                if file.endswith(".png"):
                    os.remove(os.path.join("Temp", file))
            final_page_count = total_pages
        else:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Drawing slides (MP)...")
            required_pages = math.ceil(total_images / slides_per_page)
            processed_pages_ref = Value('i', 0)
            processed_pages_lock = Lock()
            animation_stopped3 = False
            animation_thread3 = Thread(target=loading_animation3, args=(processed_pages_ref, required_pages, processed_pages_lock))
            animation_thread3.start()
            processes = []
            output_parts = []
            current_start_page = 1
            pages_per_process = required_pages // 5
            leftover = required_pages % 5
            for i in range(5):
                if pages_per_process > 0:
                    current_end_page = current_start_page + pages_per_process - 1
                    output_pdf_path = os.path.join(TEMP_FOLDER, f"{i+1}.pdf")
                    p = Process(target=draw_slides_pages_worker, args=(
                        current_start_page,
                        current_end_page,
                        slides_per_page,
                        layout_params,
                        total_images,
                        TEMP_FOLDER,
                        output_pdf_path,
                        processed_pages_ref,
                        processed_pages_lock
                    ))
                    processes.append(p)
                    output_parts.append(output_pdf_path)
                    p.start()
                    current_start_page = current_end_page + 1
                else:
                    break
            if leftover > 0:
                current_end_page = current_start_page + leftover - 1
                output_pdf_path = os.path.join(TEMP_FOLDER, "6.pdf")
                p = Process(target=draw_slides_pages_worker, args=(
                    current_start_page,
                    current_end_page,
                    slides_per_page,
                    layout_params,
                    total_images,
                    TEMP_FOLDER,
                    output_pdf_path,
                    processed_pages_ref,
                    processed_pages_lock
                ))
                processes.append(p)
                output_parts.append(output_pdf_path)
                p.start()
            for p in processes:
                p.join()
                if p.exitcode != 0:
                    logging.error(f"Process {p.pid} exited with code {p.exitcode}")
                    print(f"{Fore.RED}{Style.BRIGHT}An error occurred in one of the processes (PID: {p.pid}). Check logs for details.")
                    return
            time.sleep(0.1)
            animation_stopped3 = True
            animation_thread3.join()
            print(f"{Fore.MAGENTA}{Style.BRIGHT}\n\nCleaning up...")
            for file in os.listdir("Temp"):
                if file.endswith(".png"):
                    os.remove(os.path.join("Temp", file))
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Saving final PDF...")
            final_pdf = fitz.open()
            for part in natsorted(output_parts, alg=ns.IGNORECASE):
                with fitz.open(part) as part_pdf:
                    final_pdf.insert_pdf(part_pdf)
            final_pdf.save(output_path)
            final_pdf.close()
            logging.info("Drawing slides completed")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}\nCleaning up...")
            for part in output_parts:
                try:
                    os.remove(part)
                    logging.info(f"Deleted temporary output part: {part}")
                except Exception as e:
                    logging.warning(f"Could not remove temporary file {part}: {e}")
        if remove_first_slides and indicate_stars:
            add_star_symbols(output_path, slides_per_page)
        if cover_merge:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Inserting cover page...")
            cover_pdf_path = os.path.join(TEMP_FOLDER, "cover_page.pdf")
            if os.path.exists(cover_pdf_path):
                cover_pdf = fitz.open(cover_pdf_path)
                cover_page_count = cover_pdf.page_count
                final_pdf = fitz.open(output_path)
                final_pdf.insert_pdf(cover_pdf, from_page=0, to_page=cover_page_count - 1, start_at=0)
                final_pdf.set_page_labels([])
                final_pdf.saveIncr()
                final_pdf.close()
                cover_pdf.close()
                logging.info("Cover page added successfully.")
                final_page_count = required_pages + cover_page_count
            else:
                final_page_count = required_pages
        else:
            final_page_count = required_pages
        total_time = format_time(time.time() - start_time)
        show_merge_summary(total_page, final_page_count, output_path, pdf_count, total_time)
    except Exception as e:
        logging.error(f"Error processing merged PDF: {e}")
        raise
    return output_path

# ---------------- Main Program ----------------
def main():
    global animation_stopped, animation_stopped2, animation_stopped3, animation_stopped_resizing, animation_stopped_drawing
    global remove_first_slides, indicate_stars
    animation_stopped = False
    animation_stopped2 = False
    animation_stopped3 = False
    animation_stopped_resizing = False
    animation_stopped_drawing = False
    try:
        remove_previous_logs()
        clear_console()
        print(rf"""{Fore.CYAN}{Style.BRIGHT}  __  __ ______ _____   _____ ______ _____ 
 |  \/  |  ____|  __ \ / ____|  ____|  __ \ 
 | \  / | |__  | |__) | |  __| |__  | |__) |
 | |\/| |  __| |  _  /| | |_ |  __| |  _  / 
 | |  | | |____| | \ \| |__| | |____| | \ \ 
 |_|  |_|______|_|  \_\\_____|______|_|  \_\
         """)
        free_storage = check_free_storage()
        print(f"  V4.0 | Free : {free_storage} | © Afnan Tawsif\n")
        print(f"{Fore.YELLOW}{Style.BRIGHT}+---------------------------+\n"
              "|   PDF and slides merger   |\n"
              "+---------------------------+\n"
              "| 1. Merge PDFs             |\n"
              "| 2. Merge class slides     |\n"
              "+---------------------------+\n")
        choice = input("Enter your choice: ")
        if choice == '1':
            clear_console()
            print("Merging PDFs...")
            try:
                merge_pdfs_to_result()
            except Exception as e:
                animation_stopped = True
                print(f"{Fore.RED}{Style.BRIGHT}An error occurred while merging PDFs.")
                logging.error(f"Error merging PDFs: {e}")
        elif choice == '2':
            clear_console()
            print(f"{Fore.YELLOW}{Style.BRIGHT}+-------------------------------+\n"
                  "|     Slide count in a page     |\n"
                  "+-------------------------------+\n"
                  "| A. 3 (A4-Portrait output)     |\n"
                  "| B. 4 (A4-Landscape output)    |\n"
                  "+-------------------------------+\n")
            slide_count_choice = input("Enter your choice: ").strip().upper()
            if slide_count_choice not in ['A', 'B']:
                print(f"{Fore.RED}{Style.BRIGHT}Invalid slide count choice!")
                logging.warning("Invalid slide count choice entered.")
                return
            clear_console()
            print(f"{Fore.YELLOW}{Style.BRIGHT}+------------------------------+\n"
                  "|      Remove 1st slides?      |\n"
                  "|    (usually cover slides)    |\n"
                  "+------------------------------+\n"
                  "| A. Yes                       |\n"
                  "| B. No                        |\n"
                  "+------------------------------+\n")
            remove_choice = input("Enter your choice: ").strip().upper()
            if remove_choice not in ['A', 'B']:
                print(f"{Fore.RED}{Style.BRIGHT}Invalid 1st slide choice!")
                logging.warning("Invalid 1st slide choice entered.")
                return
            remove_first_slides = (remove_choice == 'A')
            if remove_first_slides:
                print(f"{Fore.YELLOW}{Style.BRIGHT}\n+----------------------------------+\n"
                      "|  Indicate beginning of new pdf?  |\n"
                      "+----------------------------------+\n"
                      "| A. Yes                           |\n"
                      "| B. No                            |\n"
                      "+----------------------------------+\n"
                      f"{Fore.RED}{Style.BRIGHT}Note: This works as an alternative of cover slides.\n")
                indicate_choice = input(f"{Fore.YELLOW}{Style.BRIGHT}Enter your choice: ").strip().upper()
                if indicate_choice not in ['A', 'B']:
                    print(f"{Fore.RED}{Style.BRIGHT}Invalid indication choice!")
                    logging.warning("Invalid indication choice entered.")
                    return
                indicate_stars = (indicate_choice == 'A')
            clear_console()
            print(f"{Fore.YELLOW}{Style.BRIGHT}+-----------------------------------+\n"
                  "|          Select strategy          |\n"
                  "+-----------------------------------+\n"
                  f"| A. Vector Assembly {Fore.GREEN}{Style.BRIGHT}(Recommended){Fore.YELLOW}{Style.BRIGHT}  |\n"
                  "| B. Pixel Construct                |\n"
                  "+-----------------------------------+\n"
                  f"{Fore.YELLOW}{Style.BRIGHT}+--------------------+-------+\n"
                  f"|     Factors        | A | B |\n"
                  f"+--------------------+-------+\n"
                  f"| Raw slide quality  | {Fore.GREEN}{Style.BRIGHT}√ {Fore.YELLOW}{Style.BRIGHT}| {Fore.RED}{Style.BRIGHT}× {Fore.YELLOW}{Style.BRIGHT}|\n"
                  f"| Low resource usage | {Fore.GREEN}{Style.BRIGHT}√ {Fore.YELLOW}{Style.BRIGHT}| {Fore.RED}{Style.BRIGHT}× {Fore.YELLOW}{Style.BRIGHT}|\n"
                  f"| Time efficient     | {Fore.GREEN}{Style.BRIGHT}√ {Fore.YELLOW}{Style.BRIGHT}| {Fore.RED}{Style.BRIGHT}× {Fore.YELLOW}{Style.BRIGHT}|\n"
                  f"| Sumatra pdf viewer | {Fore.GREEN}{Style.BRIGHT}√ {Fore.YELLOW}{Style.BRIGHT}| {Fore.GREEN}{Style.BRIGHT}√ {Fore.YELLOW}{Style.BRIGHT}|\n"
                  f"| Adobe pdf viewer   | {Fore.RED}{Style.BRIGHT}× {Fore.YELLOW}{Style.BRIGHT}| {Fore.GREEN}{Style.BRIGHT}√ {Fore.YELLOW}{Style.BRIGHT}|\n"
                  f"| Adobe pdf print    | {Fore.GREEN}{Style.BRIGHT}√ {Fore.YELLOW}{Style.BRIGHT}| {Fore.GREEN}{Style.BRIGHT}√ {Fore.YELLOW}{Style.BRIGHT}|\n"
                  f"+--------------------+-------+\n")
            strategy_choice = input("Enter your choice: ").strip().upper()
            if strategy_choice not in ['A', 'B']:
                print(f"{Fore.RED}{Style.BRIGHT}Invalid strategy choice!")
                logging.warning("Invalid strategy choice entered.")
                return
            if strategy_choice == 'A':
                clear_console()
                print(f"{Fore.YELLOW}{Style.BRIGHT}+---------------------------+\n"
                      "|     Colour inversion?     |\n"
                      "+---------------------------+\n"
                      "| A. Yes                    |\n"
                      "| B. No                     |\n"
                      "+---------------------------+\n")
                invert_choice = input("Enter your choice: ").strip().upper()
                if invert_choice not in ['A', 'B']:
                    print(f"{Fore.RED}{Style.BRIGHT}Invalid choice for colour inversion!")
                    logging.warning("Invalid color inversion choice entered.")
                    return
                invert_colors = (invert_choice == 'A')
                clear_console()
                print(f"{Fore.YELLOW}{Style.BRIGHT}+---------------------------+\n"
                      "|        Cover page?        |\n"
                      "+---------------------------+\n"
                      "| A. Yes                    |\n"
                      "| B. No                     |\n"
                      "+---------------------------+\n")
                cover_choice = input("Enter your choice: ").strip().upper()
                if cover_choice not in ['A', 'B']:
                    print(f"{Fore.RED}{Style.BRIGHT}Invalid cover page choice!")
                    logging.warning("Invalid cover page choice entered.")
                    return
                if cover_choice == 'A':
                    page_orientation = "Portrait" if slide_count_choice == 'A' else "Landscape"
                    create_cover_page(page_orientation)
                clear_console()
                print(f"{Fore.RED}{Style.BRIGHT}Merging class slides using Vector Assembly with color inversion {'ON' if invert_colors else 'OFF'}.")
                try:
                    vector_assembly_slides_merger(slide_count_choice, invert_colors, cover_merge=(cover_choice == 'A'))
                except Exception as e:
                    animation_stopped_drawing = True
                    print(f"{Fore.RED}{Style.BRIGHT}An error occurred while merging slides.")
                    logging.error(f"Error merging slides (Vector Assembly): {e}")
            elif strategy_choice == 'B':
                clear_console()
                print(f"{Fore.YELLOW}{Style.BRIGHT}+---------------------------------+\n"
                      "|        Select Output DPI        |\n"
                      "+---------------------------------+\n"
                      "| A. 200 dpi                      |\n"
                      f"| B. 300 dpi {Fore.GREEN}{Style.BRIGHT}(Print standard){Fore.YELLOW}{Style.BRIGHT}     |\n"
                      "| C. 600 dpi                      |\n"
                      "+---------------------------------+\n"
                      f"{Fore.RED}{Style.BRIGHT}Note: Higher DPI increases processing time and memory usage.\n")
                quality_choice = input(f"{Fore.YELLOW}{Style.BRIGHT}Enter your choice: ").strip().upper()
                if quality_choice not in ['A', 'B', 'C']:
                    print(f"{Fore.RED}{Style.BRIGHT}Invalid DPI choice!")
                    logging.warning("Invalid DPI choice entered.")
                    return
                dpi_mapping = {'A': 200, 'B': 300, 'C': 600}
                dpi = dpi_mapping[quality_choice]
                clear_console()
                print(f"{Fore.YELLOW}{Style.BRIGHT}+---------------------------+\n"
                      "|     Colour inversion?     |\n"
                      "+---------------------------+\n"
                      "| A. Yes                    |\n"
                      "| B. No                     |\n"
                      "+---------------------------+\n")
                invert_choice = input("Enter your choice: ").strip().upper()
                if invert_choice not in ['A', 'B']:
                    print(f"{Fore.RED}{Style.BRIGHT}Invalid choice for colour inversion!")
                    logging.warning("Invalid color inversion choice entered.")
                    return
                invert_colors = (invert_choice == 'A')
                clear_console()
                print(f"{Fore.YELLOW}{Style.BRIGHT}+---------------------------+\n"
                      "|        Cover page?        |\n"
                      "+---------------------------+\n"
                      "| A. Yes                    |\n"
                      "| B. No                     |\n"
                      "+---------------------------+\n")
                cover_choice = input("Enter your choice: ").strip().upper()
                if cover_choice not in ['A', 'B']:
                    print(f"{Fore.RED}{Style.BRIGHT}Invalid cover page choice!")
                    logging.warning("Invalid cover page choice entered.")
                    return
                if cover_choice == 'A':
                    page_orientation = "Portrait" if slide_count_choice == 'A' else "Landscape"
                    create_cover_page(page_orientation)
                clear_console()
                print(f"{Fore.RED}{Style.BRIGHT}Merging class slides at {dpi} DPI with color inversion {'ON' if invert_colors else 'OFF'}")
                try:
                    acs_class_slides_merger(slide_count_choice, dpi, invert_colors, cover_merge=(cover_choice == 'A'))
                    logging.info(f"Started merging class slides in Pixel Construct mode with color inversion {'ON' if invert_colors else 'OFF'}.")
                except Exception as e:
                    animation_stopped2 = True
                    animation_stopped3 = True
                    print(f"{Fore.RED}{Style.BRIGHT}An error occurred while merging slides.")
                    logging.error(f"Error merging slides (Pixel Construct): {e}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Invalid choice!")
            logging.warning("Invalid choice entered.")
            return
    except Exception as e:
        animation_stopped = True
        print(f"{Fore.RED}{Style.BRIGHT}An error occurred: {e}")
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    while True:
        main()
        print()
        input(f"{Fore.RED}{Style.BRIGHT}Press Enter to restart program.")
        clear_console()

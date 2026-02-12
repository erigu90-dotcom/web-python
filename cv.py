import os
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw

app = Flask(__name__)

##set up folder for uploaded photos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Ccreat folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_image_round(input_path, output_path, size=(300, 300)):
    img = Image.open(input_path).convert("RGBA")
    img = img.resize(size)

    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    img.putalpha(mask)
    img.save(output_path, format="PNG")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = str(request.form.get("name",""))
        ocupation = str(request.form.get("ocupation",""))
        email = str(request.form.get("email",""))
        phone = str(request.form.get("phone",""))
        website = str(request.form.get("website",""))
        skills1 = str(request.form.get("skills1",""))
        skills2 = str(request.form.get("skills2",""))
        skills3 = str(request.form.get("skills3",""))
        interests1 = str(request.form.get("interests1",""))
        interests2 = str(request.form.get("interests2",""))
        interests3 = str(request.form.get("interests3",""))
        profile = str(request.form.get("profile",""))
        experience_position = str(request.form.get("experience_position",""))
        experience_company = str(request.form.get("experience_company",""))
        experience_date = str(request.form.get("experience_date",""))
        experience_role = str(request.form.get("experience_role",""))
        experience_position2 = str(request.form.get("experience_position2",""))
        experience_company2 = str(request.form.get("experience_company2",""))
        experience_date2 = str(request.form.get("experience_date2",""))
        experience_role2 = str(request.form.get("experience_role2",""))
        education1 = str(request.form.get("education1",""))
        education_institute1 = str(request.form.get("education_institute1",""))
        education1_date_degree = str(request.form.get("education1_date_degree",""))
        portfolio1 = str(request.form.get("portfolio1",""))
        portfolio1_text = str(request.form.get("portfolio1_text",""))
        
        # ====== FOTO ======
        photo = request.files.get("photo")
        photo_path = None
        round_photo_path = None

        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            photo.save(photo_path)
            
            round_photo_path = os.path.join(
            app.config["UPLOAD_FOLDER"], "round_" + filename)
            make_image_round(photo_path, round_photo_path)

        # Limitar longitudes
        profile = profile[:220]
        experience_role = experience_role[:140]
        experience_role2 = experience_role2[:140]

        # Generar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.image("cveng.png", x=0, y=0, w=210)
        if round_photo_path:
            pdf.image(round_photo_path, x=12, y=12, w=60, h=60)
            
    ## Nombre y ocupación
        pdf.set_font_size(16)
        pdf.set_font(style="B")
        pdf.set_text_color(250, 195, 2)
        pdf.set_xy(15, 80)
        pdf.multi_cell(w=55, h=5, txt=name, border=0, align="C")
    ## Ocupación
        pdf.set_font_size(12)
        pdf.set_xy(15, 95)
        pdf.set_text_color(255, 255, 255)
        pdf.multi_cell(w=55, h=5, txt=ocupation, border=0, align="C")
    
    # Datos de contacto y habilidades
        pdf.set_font_size(12)
        pdf.set_text_color(255, 255, 255)
        pdf.text(20,143, email)
        pdf.text(20,159, phone)
        pdf.text(20,173, website)
        pdf.text(20,210, skills1)
        pdf.text(20,220, skills2)
        pdf.text(20,230, skills3)
        pdf.text(20,265, interests1)
        pdf.text(20,275, interests2)
        pdf.text(20,285, interests3)
        
    ## Perfil Profesional
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(34, 42, 53)
        pdf.set_xy(95, 30)
        pdf.multi_cell(w=100, h=5, txt=profile, border=0)
   
    ## Experiencia Laboral
        pdf.set_font("Arial", size=12, style="B")
        pdf.set_xy(108, 95)
        pdf.multi_cell(w=90, h=5, txt=experience_position)
        
        pdf.set_font("Arial", size=12, style="B")
        pdf.set_x(108)
        pdf.multi_cell(w=90, h=5, txt=experience_company)
        
        pdf.set_font("Arial", size=12,)
        pdf.set_x(108)
        pdf.multi_cell(w=90, h=5, txt=experience_date)
        pdf.ln(2)
        pdf.set_x(108)
        pdf.multi_cell(w=90, h=5, txt=experience_role)

    ## Experiencia Laboral2
        pdf.set_font("Arial", size=12, style="B")
        pdf.set_xy(108, 140)
        pdf.multi_cell(w=90, h=5, txt=experience_position2)
        
        pdf.set_font("Arial", size=12, style="B")
        pdf.set_x(108)
        pdf.multi_cell(w=90, h=5, txt=experience_company2)
        
        pdf.set_font("Arial", size=12,)
        pdf.set_x(108)
        pdf.multi_cell(w=90, h=5, txt=experience_date2)
        pdf.ln(2)
        pdf.set_x(108)
        pdf.multi_cell(w=90, h=5, txt=experience_role2)
    
    ## Educación
        pdf.set_font("Arial", size=12, style="B")
        pdf.set_xy(108, 198)
        pdf.multi_cell(w=90, h=5, txt=education1)
        
        pdf.set_font("Arial", size=12, style="B")
        pdf.set_xy(108, 204)
        pdf.multi_cell(w=90, h=5, txt=education_institute1)
        
        pdf.set_font("Arial", size=12,)
        pdf.set_xy(108, 210)
        pdf.multi_cell(w=90, h=5, txt=education1_date_degree)


    ## Portafolio
        pdf.set_font("Arial", size=12, style="B")
        pdf.set_xy(95, 242)
        pdf.multi_cell(w=90, h=5, txt=portfolio1)
        
        pdf.set_font("Arial", size=12,)
        pdf.set_xy(95, 249)
        pdf.multi_cell(w=90, h=5, txt=portfolio1_text)

        filename = f"cv_{name.replace(' ', '_')}.pdf"
        pdf.output(filename)

        for path in [photo_path, round_photo_path]:
            if path and os.path.exists(path):
                os.remove(path)
        
        return render_template(
            "cv.html",
            name=name,
            ocupation=ocupation,
            email=email,
            phone=phone,
            website=website,
            skills1=skills1,
            skills2=skills2,
            skills3=skills3,
            interests1=interests1,
            interests2=interests2,
            interests3=interests3,
            profile=profile,
            experience_position=experience_position,
            experience_company=experience_company,
            experience_date=experience_date,
            experience_role=experience_role,
            experience_position2=experience_position2,
            experience_company2=experience_company2,
            experience_date2=experience_date2,
            experience_role2=experience_role2,
            education1=education1,
            education_institute1=education_institute1,
            education1_date_degree=education1_date_degree,
            portfolio1=str(request.form.get("portfolio1","")),
            portfolio1_text=str(request.form.get("portfolio1_text","")),
        )

    # GET request -> siempre devuelve template
    return render_template("cv.html")
@app.route("/descargar")
def descargar_pdf():
    return send_file("cvfilename.pdf",as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

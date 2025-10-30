# app.py

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Cargar la "Base de Datos" (simulada con CSV)
try:
    # CLAVE: Añadir 'sep=;' y 'engine="python"' para mayor control en archivos sucios
    DF_BASE = pd.read_csv('basedatos.csv', 
                          encoding='latin-1', 
                          sep=';', 
                          engine='python') 
except FileNotFoundError:
    DF_BASE = pd.DataFrame()


# 1. frmMenu (Ruta Principal)
@app.route('/')
def frmMenu():
    return render_template('frmMenu.html')

# 2. frmInstrucciones
@app.route('/instrucciones', methods=['GET'])
@app.route('/instrucciones/<matricula_id>', methods=['GET'])
def frmInstrucciones(matricula_id=None):
    # Si se pasa una matrícula, la pasamos a la plantilla; si no, mostramos la vista vacía
    if matricula_id:
        return render_template('frmInstrucciones.html', matricula=matricula_id)
    return render_template('frmInstrucciones.html')

# 3. frmAlumno (Entrada de Datos del Alumno)
@app.route('/alumno', methods=['GET'])
def frmAlumno():
    return render_template('frmAlumno.html')

# app.py (fragmento de la función procesar_frmAlumno)

# app.py (Dentro de procesar_frmAlumno)

@app.route('/alumno', methods=['POST'])
def procesar_frmAlumno():
    nombre = request.form.get('nombre')
    matricula = request.form.get('matricula')
    carrera = request.form.get('carrera') 
    
    global DF_BASE 
    # Usamos los nombres de columna EXACTOS
    nuevo_registro = pd.DataFrame([{
        'NOMBRE': nombre,            
        'CONTROL': matricula,         
        'CARRERA': carrera,         
        'Puntaje_Total': 0, 
        'Resultado': 'PENDIENTE'
        # NOTA: Aquí faltarían el resto de las columnas (CAMPO1, CAMPO2, etc.)
    }])
    
    DF_BASE = pd.concat([DF_BASE, nuevo_registro], ignore_index=True)
    
    # Guardar con sep=';' y encoding='latin-1'
    DF_BASE.to_csv('basedatos.csv', index=False, encoding='latin-1', sep=';') 
    
    return redirect(url_for('frmInstrucciones', matricula_id=matricula))


# Ajustamos la ruta GET de frmUno para recibir la matrícula
# 4. frmUno (Sección 1 del Test)
@app.route('/test/uno/<matricula_id>', methods=['GET'])
def frmUno(matricula_id):
    # Lógica GET: Cargar las preguntas para la vista
    return render_template('frmUno.html', 
                           matricula=matricula_id, 
                           preguntas=PREGUNTAS_FRM_UNO)



@app.route('/test/uno', methods=['POST'])
def procesar_frmUno():
    matricula = request.form.get('matricula_id')
    global DF_BASE
    
    # 1. Recolección de respuestas (1, 0, o -1)
    respuestas_uno = {}
    
    for i in range(1, 11):
        nombre_campo_html = f'q{i}'
        valor_respuesta_str = request.form.get(nombre_campo_html)
        
        if valor_respuesta_str is None:
            # Validación obligatoria del test
            return "Error: Por favor, responda todas las preguntas antes de continuar.", 400
        
        # Guardamos la respuesta en una columna R_U_Qx
        respuestas_uno[f'R_U_Q{i}'] = int(valor_respuesta_str)
        
    # 2. Actualizar el DataFrame con las 10 respuestas
    
    # Encontrar el índice de la fila por CONTROL
    indice_fila = DF_BASE[DF_BASE['CONTROL'] == matricula].index

    if not indice_fila.empty:
        # Actualizar la fila con todas las respuestas
        for key, value in respuestas_uno.items():
            # Usar .loc para actualizar la fila
            DF_BASE.loc[indice_fila, key] = value
        
        # Opcional: Guardar el CSV actualizado (para mantener el progreso en caso de fallo)
        DF_BASE.to_csv('basedatos.csv', index=False, encoding='latin-1', sep=';') 

    # 3. Redirigir al siguiente formulario del test
    return redirect(url_for('frmDos', matricula_id=matricula))


# 5. frmDos (Sección 2 del Test)
@app.route('/test/dos/<matricula_id>', methods=['GET'])
def frmDos(matricula_id):
    # Lógica GET: Cargar las preguntas para la vista
    global PREGUNTAS_FRM_DOS # Asegúrate de que esta lista esté definida al inicio
    return render_template('frmDos.html', 
                           matricula=matricula_id, 
                           preguntas=PREGUNTAS_FRM_DOS)

@app.route('/test/dos', methods=['POST'])
def procesar_frmDos():
    matricula = request.form.get('matricula_id')
    global DF_BASE
    
    # 1. Recolección de respuestas (Preguntas 11 a 20)
    respuestas_dos = {}
    
    # Iterar de 1 a 10 para mapear a R_D_Q1 a R_D_Q10, pero el campo HTML es q11 a q20
    for i in range(1, 11):
        # El nombre en el HTML es 'q11', 'q12', etc.
        nombre_campo_html = f'q{i + 10}'
        valor_respuesta_str = request.form.get(nombre_campo_html)
        
        if valor_respuesta_str is None:
            return "Error: Por favor, responda todas las preguntas antes de continuar.", 400
        
        # El nombre de la columna en el DF será R_D_Q1, R_D_Q2, etc.
        respuestas_dos[f'R_D_Q{i}'] = int(valor_respuesta_str)
        
    # 2. Actualizar el DataFrame con las 10 respuestas
    indice_fila = DF_BASE[DF_BASE['CONTROL'] == matricula].index

    if not indice_fila.empty:
        for key, value in respuestas_dos.items():
            DF_BASE.loc[indice_fila, key] = value
        
    # 3. Redirigir al siguiente formulario del test
    return redirect(url_for('frmTres', matricula_id=matricula))




# 6. frmTres (Sección 3 del Test)
@app.route('/test/tres/<matricula_id>', methods=['GET'])
def frmTres(matricula_id):
    # Lógica GET: Cargar las preguntas para la vista
    global PREGUNTAS_FRM_TRES
    return render_template('frmTres.html', 
                           matricula=matricula_id, 
                           preguntas=PREGUNTAS_FRM_TRES)

@app.route('/test/tres', methods=['POST'])
def procesar_frmTres():
    matricula = request.form.get('matricula_id')
    global DF_BASE
    
    # 1. Recolección de respuestas (Preguntas 21 a 30)
    respuestas_tres = {}
    
    # Iterar de 1 a 10 para mapear a R_T_Q1 a R_T_Q10. El campo HTML es q21 a q30
    for i in range(1, 11):
        # El nombre en el HTML es 'q21', 'q22', etc.
        nombre_campo_html = f'q{i + 20}'
        valor_respuesta_str = request.form.get(nombre_campo_html)
        
        if valor_respuesta_str is None:
            return "Error: Por favor, responda todas las preguntas antes de continuar.", 400
        
        # El nombre de la columna en el DF será R_T_Q1, R_T_Q2, etc.
        respuestas_tres[f'R_T_Q{i}'] = int(valor_respuesta_str)
        
    # 2. Actualizar el DataFrame con las 10 respuestas
    indice_fila = DF_BASE[DF_BASE['CONTROL'] == matricula].index

    if not indice_fila.empty:
        for key, value in respuestas_tres.items():
            # Usar .loc para actualizar la fila
            DF_BASE.loc[indice_fila, key] = value
    # 3. Redirigir al siguiente formulario del test
    return redirect(url_for('frmCuatro', matricula_id=matricula))





# frmCuatro (Sección 4 del Test)
@app.route('/test/cuatro/<matricula_id>', methods=['GET'])
def frmCuatro(matricula_id):
    # Lógica GET: Cargar las preguntas para la vista
    global PREGUNTAS_FRM_CUATRO
    return render_template('frmCuatro.html', 
                           matricula=matricula_id, 
                           preguntas=PREGUNTAS_FRM_CUATRO)

@app.route('/test/cuatro', methods=['POST'])
def procesar_frmCuatro():
    matricula = request.form.get('matricula_id')
    global DF_BASE
    
    # 1. Recolección de respuestas (Preguntas 31 a 40)
    respuestas_cuatro = {}
    
    # Iterar de 1 a 10 para mapear a R_C_Q1 a R_C_Q10. El campo HTML es q31 a q40
    for i in range(1, 11):
        # El nombre en el HTML es 'q31', 'q32', etc.
        nombre_campo_html = f'q{i + 30}'
        valor_respuesta_str = request.form.get(nombre_campo_html)
        
        if valor_respuesta_str is None:
            return "Error: Por favor, responda todas las preguntas antes de continuar.", 400
        
        # El nombre de la columna en el DF será R_C_Q1, R_C_Q2, etc. (Respuestas Cuatro)
        respuestas_cuatro[f'R_C_Q{i}'] = int(valor_respuesta_str)
        
    # 2. Actualizar el DataFrame con las 10 respuestas
    indice_fila = DF_BASE[DF_BASE['CONTROL'] == matricula].index

    if not indice_fila.empty:
        for key, value in respuestas_cuatro.items():
            # Usar .loc para actualizar la fila
            DF_BASE.loc[indice_fila, key] = value
        
        # Opcional: Guardar el CSV actualizado
        # DF_BASE.to_csv('basedatos.csv', index=False, encoding='latin-1', sep=';') 

    # 3. Redirigir al siguiente formulario del test
    return redirect(url_for('frmCinco', matricula_id=matricula))



@app.route('/test/cinco/<matricula_id>', methods=['GET'])
def frmCinco(matricula_id):
    # Lógica GET: Cargar las preguntas para la vista
    global PREGUNTAS_FRM_CINCO
    return render_template('frmCinco.html', 
                           matricula=matricula_id, 
                           preguntas=PREGUNTAS_FRM_CINCO)

@app.route('/test/cinco', methods=['POST'])
def procesar_frmCinco():
    matricula = request.form.get('matricula_id')
    global DF_BASE
    
    # 1. Recolección de respuestas (Preguntas 41 a 50)
    respuestas_cinco = {}
    
    # Iterar de 1 a 10 para mapear a R_CI_Q1 a R_CI_Q10. El campo HTML es q41 a q50
    for i in range(1, 11):
        # El nombre en el HTML es 'q41', 'q42', etc.
        nombre_campo_html = f'q{i + 40}'
        valor_respuesta_str = request.form.get(nombre_campo_html)
        
        if valor_respuesta_str is None:
            return "Error: Por favor, responda todas las preguntas antes de continuar.", 400
        
        # El nombre de la columna en el DF será R_CI_Q1, R_CI_Q2, etc. (Respuestas Cinco)
        respuestas_cinco[f'R_CI_Q{i}'] = int(valor_respuesta_str)
        
    # 2. Actualizar el DataFrame con las 10 respuestas
    indice_fila = DF_BASE[DF_BASE['CONTROL'] == matricula].index

    if not indice_fila.empty:
        for key, value in respuestas_cinco.items():
            DF_BASE.loc[indice_fila, key] = value
        
        # Opcional: Guardar el CSV actualizado
        # DF_BASE.to_csv('basedatos.csv', index=False, encoding='latin-1', sep=';') 

    # 3. Redirigir al siguiente formulario del test
    return redirect(url_for('frmSeis', matricula_id=matricula))




# app.py (Fragmento - Añade estas funciones)

# 9. frmSeis (Sección 6 del Test - FINAL)
@app.route('/test/seis/<matricula_id>', methods=['GET'])
def frmSeis(matricula_id):
    global PREGUNTAS_FRM_SEIS
    return render_template('frmSeis.html', 
                           matricula=matricula_id, 
                           preguntas=PREGUNTAS_FRM_SEIS)

@app.route('/test/seis', methods=['POST'])
def procesar_frmSeis():
    matricula = request.form.get('matricula_id')
    global DF_BASE
    
    # --- PASO 1: Guardar las Respuestas de la Sección 6 (R_S_Qx) ---
    respuestas_seis = {}
    for i in range(1, 11):
        nombre_campo_html = f'q{i + 50}'
        valor_respuesta_str = request.form.get(nombre_campo_html)
        
        if valor_respuesta_str is None:
            return "Error: Por favor, responda todas las preguntas antes de FINALIZAR.", 400
        
        respuestas_seis[f'R_S_Q{i}'] = int(valor_respuesta_str)
    
    indice_fila = DF_BASE[DF_BASE['CONTROL'] == matricula].index

    if not indice_fila.empty:
        # Actualizar el DataFrame con las 10 respuestas de la Sección 6
        for key, value in respuestas_seis.items():
            DF_BASE.loc[indice_fila, key] = value
            
        # --- PASO 2: LÓGICA DE CÁLCULO FINAL (Traducción de ObtenerResultado) ---
        
        # 1. Definir los nombres de las columnas de respuesta para cada sección
        secciones = ['R_U', 'R_D', 'R_T', 'R_C', 'R_CI', 'R_S']
        
        # 2. Iterar sobre los 10 Campos (Columna CAMPO1 a CAMPO10)
        for campo_index in range(1, 11):
            
            # El puntaje de cada campo es la suma de la pregunta 'campo_index' en las 6 secciones
            puntaje_acumulado = 0
            
            for seccion_prefix in secciones:
                columna_respuesta = f'{seccion_prefix}_Q{campo_index}'
                
                # Se accede al valor de la celda de la fila actual (indice_fila)
                # NOTA: .iloc[0] obtiene el valor porque indice_fila es un array de un solo elemento.
                try:
                    valor_q = DF_BASE.loc[indice_fila, columna_respuesta].iloc[0]
                    # Convertir a entero (si Pandas no lo hizo) y acumular
                    puntaje_acumulado += int(valor_q)
                except KeyError:
                    # Esto ocurre si falta alguna columna (R_U_Q1, etc.)
                    print(f"Error: Columna {columna_respuesta} no encontrada. Revise encabezado CSV.")
                    pass 

            # 3. Aplicar la Clasificación (ALTA, MEDIA, BAJA)
            if puntaje_acumulado >= 3: # Rango original: > 2
                clasificacion = "ALTA"
            elif puntaje_acumulado >= -2 and puntaje_acumulado <= 2: # Rango original: -2 <= x <= 2
                clasificacion = "MEDIA"
            else: # Rango original: <= -3
                clasificacion = "BAJA"

            # 4. Guardar la clasificación final en la columna CAMPOx
            campo_nombre = f'CAMPO{campo_index}'
            DF_BASE.loc[indice_fila, campo_nombre] = clasificacion
            
        # --- PASO 3: Guardar el Resultado Final y Redirigir ---
        
        # Guardar la fecha (Columna 14, que en tu CSV es 'FECHA')
        DF_BASE.loc[indice_fila, 'FECHA'] = pd.to_datetime('today').strftime('%d/%m/%Y')
        
        # Guardar el resultado final en el CSV
        DF_BASE.to_csv('basedatos.csv', index=False, encoding='latin-1', sep=';') 

        # Redirigir al formulario de resultados con la matrícula
        return redirect(url_for('frmResultados', matricula_id=matricula))

    else:
        # Caso de seguridad si no se encuentra el alumno
        return "Error: Matrícula no encontrada durante el procesamiento final.", 500





# 7. frmBuscar (Búsqueda de Resultados)
# app.py (Fragmento - Busca la función frmBuscar)

@app.route('/buscar', methods=['GET', 'POST'])
def frmBuscar():
    global DF_BASE
    
    # ¡CORRECCIÓN AQUÍ! Usar 'NOMBRE' en mayúsculas.
    nombres_alumnos = DF_BASE['NOMBRE'].dropna().unique().tolist() 
    
    if request.method == 'POST':
        nombre_buscado = request.form.get('nombre_alumno')
        
        # ¡CORRECCIÓN AQUÍ! Usar 'NOMBRE' para la búsqueda.
        registro = DF_BASE[DF_BASE['NOMBRE'] == nombre_buscado] 
        
        if not registro.empty:
            # ¡CORRECCIÓN AQUÍ! Usar 'CONTROL' en mayúsculas para la matrícula.
            matricula_encontrada = registro.iloc[0]['CONTROL']
            return redirect(url_for('frmResultados', matricula_id=matricula_encontrada))
        else:
            # Si no se encuentra (aunque esto es raro si se usa el ComboBox)
            return render_template('frmBuscar.html', 
                                   error="Resultado no encontrado.",
                                   nombres=nombres_alumnos) # Volver a pasar los nombres
            
    # Lógica GET: Muestra el formulario con la lista de nombres
    return render_template('frmBuscar.html', nombres=nombres_alumnos)




# 10. frmResultados (Muestra los resultados finales)
@app.route('/test/resultados/<matricula_id>', methods=['GET'])
def frmResultados(matricula_id):
    global DF_BASE, DESCRIPCIONES_CAMPOS_VOCACIONALES

    indice_fila = DF_BASE[DF_BASE['CONTROL'] == matricula_id].index

    if not indice_fila.empty:
        datos_alumno = DF_BASE.loc[indice_fila].iloc[0] # Obtiene la fila como una Serie
        
        resultados_campos = {}
        for i in range(1, 11):
            campo_nombre = f'CAMPO{i}'
            # Obtener la clasificación (ALTA, MEDIA, BAJA)
            clasificacion = datos_alumno.get(campo_nombre, "N/A") 
            # Obtener la descripción asociada
            descripcion = DESCRIPCIONES_CAMPOS_VOCACIONALES.get(campo_nombre, "Descripción no disponible")
            resultados_campos[campo_nombre] = {
                "clasificacion": clasificacion,
                "descripcion": descripcion
            }

        return render_template('frmResultados.html', 
                               matricula=matricula_id,
                               nombre_alumno=datos_alumno.get('NOMBRE', 'N/A'),
                               carrera_alumno=datos_alumno.get('CARRERA', 'N/A'),
                               resultados=resultados_campos)
    else:
        return "Error: Resultados no encontrados para la matrícula especificada.", 404




PREGUNTAS_FRM_UNO = [
    "Examinar, analizar y estudiar el funcionamiento de máquinas nuevas e inventos tecnológicos.",
    "Reparar equipos de sonido, ordenadores, televisores, frigoríficos, aire acondicionado, etc.",
    "Intervenir en la elaboración de contratos, escrituras y testamentos.",
    "Diagnosticar y administrar tratamientos médicos, para curar tratamientos médicos, para curar o prevenir las enfermedades de los seres humanos.",
    "Traducir e interpretar textos escritos en otro idioma.",
    "Realizar funciones de protección, seguridad y vigilancia.",
    "Desarrollar y realizar un guion cinematográfico",
    "Realizar estudios en el área de las matemáticas y la estadística",
    "Componer, dirigir o interpretar obras musicales",
    "Estudiar la evolución de las razas humanas, su organización política, social, económica y cultural (estilos artísticos, etc.)."
]
# app.py (Define las preguntas para frmDos)

PREGUNTAS_FRM_DOS = [
    "Realizar estudios e investigaciones sobre diferentes rocas", # Pregunta 11
    "Manejar máquinas de oficina (ordenador, calculadoras, etc.) y comunicaciones telefónicas", # Pregunta 12
    "Planificar, organizar, dirigir y controlar las actividades de una empresa", # Pregunta 13
    "Trabajar e interesarme por las explotaciones ganaderas y resolver sus problemas.", # Pregunta 14
    "Clasificar documentos, cartas, sellos, diapositivas u otros objetos, por temas.", # Pregunta 15
    "Entrenar o preparar a deportistas para mejorar su rendimiento", # Pregunta 16
    "Informar de los acontecimientos de actualidad", # Pregunta 17
    "Indagar y descubrir el por qué de las teorías científicas", # Pregunta 18
    "Diseñar muebles, cerámica, complementos, prendas de vestir, joyas, etc", # Pregunta 19
    "Participar en la política regional o nacional" # Pregunta 20
]

# app.py (Define las preguntas para frmTres)

PREGUNTAS_FRM_TRES = [
    "Diseñar, proyectar y elaborar los planos de un edificio en la ciudad", # Pregunta 21
    "Construir o reparar muebles u objetos de madera", # Pregunta 22
    "Dirigir o participar en las actividades de un banco", # Pregunta 23
    "Diagnosticar, prevenir y tratar las enfermedades y/o lesiones de los animales", # Pregunta 24
    "Estudiar el origen y evolución de las lenguas", # Pregunta 25
    "Perseguir, detener y poner a disposición judicial a aquellos que cometen delitos", # Pregunta 26
    "Crear o diseñar anuncios publicitarios", # Pregunta 27
    "Realizar experimentos para analizar y estudiar los fenómenos químicos y bioquímicos.", # Pregunta 28
    "Dar recitales de canto y música", # Pregunta 29
    "Dar clases en un colegio" # Pregunta 30
]

PREGUNTAS_FRM_CUATRO = [
    "Dirigir la instalación de sistemas de alarmas", # Pregunta 31
    "Realizar actividades donde se requiera habilidad manual y práctica", # Pregunta 32
    "Intervenir ante los tribunales de justicia en nombre de la ley, representando a un cliente", # Pregunta 33
    "Organizar una finca supervisando el cuidado de los animales", # Pregunta 34
    "Ordenar, clasificar y archivar documentos e informes", # Pregunta 35
    "Dirigir las competiciones deportivas y aplicar las reglas establecidas", # Pregunta 36
    "Componer, dirigir o interpretar una representación teatral, televisiva o cinematografica", # Pregunta 37
    "Hacer descubrimientos científicos.", # Pregunta 38
    "Restaurar obras de arte, tomando decisiones propias sobre la forma, modo y técnica a aplicar", # Pregunta 39
    "Investigar los problemas psicológicos de las personas" # Pregunta 40
]

PREGUNTAS_FRM_CINCO = [
    "Estudiar, proyectar y construir instalaciones eléctricas, puentes, túneles, etc", # Pregunta 41
    "Ajustar maquinaria e instalar equipos eléctricos en fábricas o edificios", # Pregunta 42
    "Asesorar sobre problemas contables, financieros y/o económicos", # Pregunta 43
    "Investigar en un laboratorio el origen de las enfermedades", # Pregunta 44
    "Organizar y clasificar libros y documentos en una biblioteca", # Pregunta 45
    "Prestar servicios en organismos y establecimientos militares", # Pregunta 46
    "Presentar las noticias en los informativos de TV", # Pregunta 47
    "Organizar la repoblación del monte seleccionando las plantas más adecuadas", # Pregunta 48
    "Crear y ejecutar pasos de danza", # Pregunta 49
    "Estudiar teorías relativas al comportamiento del ser humano" # Pregunta 50
]


PREGUNTAS_FRM_SEIS = [
    "Elaborar y diseñar programas informáticos", # Pregunta 51
    "Reparar las averías de los vehículos", # Pregunta 52
    "Aplicar los principios de la teoría económica para solucionar problemas financieros en empresas.", # Pregunta 53
    "Prescribir medicamentos para la curación de enfermedades", # Pregunta 54
    "Traducir textos de diferentes idiomas", # Pregunta 55
    "Organizar y planificar competiciones deportivas", # Pregunta 56
    "Redactar noticias, comentar informaciones y coordinar la redacción de una publicación.", # Pregunta 57
    "Investigar en un laboratorio para la creación de nuevos materiales", # Pregunta 58
    "Fotografiar, esculpir o pintar creaciones artísticas", # Pregunta 59
    "Orientar profesional y/o académicamente a las personas" # Pregunta 60
]

DESCRIPCIONES_CAMPOS_VOCACIONALES = {
    "CAMPO1": "Ingeniería industrial, de caminos, de minas, de telecomunicaciones, informáticos, técnicos de robótica, burocrática...",
    "CAMPO2": "Textil confección y piel, madera y mueble, edificación y obra civil, fabricación mecánica, mantenimiento y servicios a la producción, mantenimiento de vehículos autopropulsados.",
    "CAMPO3": "Administración",
    "CAMPO4": "Medicina, Veterinaria, Enfermería, Óptica, Biología...",
    "CAMPO5": "Intérprete, Lingüista, Biblioteconomía, Documentación, Traducción...",
    "CAMPO6": "Deportista, Policía, Animación deportiva, Entrenador/a deportivo...",
    "CAMPO7": "Comunicación, Imagen y Sonido, Comercio y Marketing",
    "CAMPO8": "Física, Estadística, Biología, Matemática, Química, Geología, Astronomía...",
    "CAMPO9": "Composición musical, instrumentistas, cantantes, decoración, restauración, diseño, paisajismo, escultura...",
    "CAMPO10": "Sociología, Psicología, Magisterio, Historia Geografía, Antropología"
}

if __name__ == '__main__':
    app.run(debug=True)
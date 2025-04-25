from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# Lista para guardar los turnos pendientes
turnos_pendientes = []

# HTML vacío, copias tu versión personalizada luego
formulario_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SmartQUEUE - Registro de Turno</title>
    <style>
        :root {
            --primary: #4361ee;
            --primary-dark: #3a56d4;
            --secondary: #7209b7;
            --accent: #4cc9f0;
            --success: #06d6a0;
            --background: #f8f9fa;
            --card-bg: #ffffff;
            --text: #2b2d42;
            --text-light: #8d99ae;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            height: 100%;
            width: 100%;
            overflow-x: hidden;
        }

        body {
            font-family: 'Poppins', 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            color: var(--text);
        }

        .container {
            width: 100%;
            max-width: 480px;
            margin: 0 auto;
        }

        .logo {
            text-align: center;
            margin-bottom: 25px;
        }

        .logo h2 {
            font-size: clamp(24px, 5vw, 28px);
            font-weight: 700;
            color: var(--primary);
            letter-spacing: -0.5px;
        }

        .logo span {
            color: var(--secondary);
        }

        .card {
            background: var(--card-bg);
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
            padding: clamp(20px, 5vw, 40px);
            position: relative;
            overflow: hidden;
            width: 100%;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 6px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
        }

        .card-decoration {
            position: absolute;
            top: 20px;
            right: 20px;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(67, 97, 238, 0.1) 0%, rgba(114, 9, 183, 0.1) 100%);
            z-index: 0;
        }

        .card-decoration:nth-child(2) {
            top: auto;
            bottom: -30px;
            right: -30px;
            width: 120px;
            height: 120px;
        }

        .card-content {
            position: relative;
            z-index: 1;
        }

        h1 {
            font-size: clamp(20px, 5vw, 24px);
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--text);
        }

        .subtitle {
            font-size: clamp(13px, 4vw, 15px);
            color: var(--text-light);
            margin-bottom: 30px;
        }

        .form-group {
            margin-bottom: 25px;
            position: relative;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-size: clamp(13px, 4vw, 14px);
            font-weight: 500;
            color: var(--text);
        }

        .input-wrapper {
            position: relative;
        }

        .input-icon {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-light);
            font-size: 18px;
        }

        input[type=text] {
            width: 100%;
            padding: 16px 16px 16px 48px;
            font-size: clamp(14px, 4vw, 15px);
            border: 2px solid #e9ecef;
            border-radius: 12px;
            background-color: #f8f9fa;
            color: var(--text);
            transition: all 0.3s ease;
            -webkit-appearance: none; /* Removes iOS default styling */
        }

        input[type=text]:focus {
            outline: none;
            border-color: var(--primary);
            background-color: #fff;
            box-shadow: 0 0 0 4px rgba(67, 97, 238, 0.15);
        }

        input[type=text]::placeholder {
            color: #adb5bd;
        }

        button {
            width: 100%;
            padding: clamp(14px, 4vw, 16px);
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: clamp(15px, 4vw, 16px);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(67, 97, 238, 0.3);
            -webkit-appearance: none; /* Removes iOS default styling */
            touch-action: manipulation; /* Improves touch response */
            min-height: 50px; /* Ensures good tap target size */
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(67, 97, 238, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        .success-message {
            margin-top: 25px;
            padding: 16px;
            background-color: rgba(6, 214, 160, 0.1);
            border-radius: 12px;
            color: var(--success);
            font-weight: 500;
            display: flex;
            align-items: center;
            animation: slideUp 0.5s ease;
            font-size: clamp(13px, 4vw, 14px);
        }

        .success-icon {
            margin-right: 12px;
            background: var(--success);
            color: white;
            min-width: 24px;
            min-height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* User icon */
        .user-icon {
            display: inline-block;
            width: 18px;
            height: 18px;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238d99ae' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'%3E%3C/path%3E%3Ccircle cx='12' cy='7' r='4'%3E%3C/circle%3E%3C/svg%3E");
            background-size: contain;
            background-repeat: no-repeat;
        }

        /* Check icon */
        .check-icon {
            display: inline-block;
            width: 14px;
            height: 14px;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
            background-size: contain;
            background-repeat: no-repeat;
        }

        /* Enhanced mobile responsiveness */
        @media (max-width: 480px) {
            .card {
                border-radius: 12px;
            }
            
            .card-decoration {
                width: 60px;
                height: 60px;
            }
            
            .card-decoration:nth-child(2) {
                width: 90px;
                height: 90px;
            }
            
            .success-message {
                padding: 12px;
            }
        }

        /* Small phones */
        @media (max-width: 360px) {
            body {
                padding: 15px;
            }
            
            .logo {
                margin-bottom: 15px;
            }
            
            .card {
                padding: 20px 15px;
            }
            
            .subtitle {
                margin-bottom: 20px;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
        }

        /* Fix for iOS input zoom */
        @media screen and (-webkit-min-device-pixel-ratio: 0) { 
            select,
            textarea,
            input[type="text"] {
                font-size: 16px;
            }
        }

        /* Landscape orientation adjustments */
        @media (max-height: 500px) and (orientation: landscape) {
            body {
                padding: 10px;
            }
            
            .container {
                padding: 0;
            }
            
            .logo {
                margin-bottom: 10px;
            }
            
            .card {
                padding: 15px;
            }
            
            .subtitle {
                margin-bottom: 15px;
            }
            
            .form-group {
                margin-bottom: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h2>Smart<span>QUEUE</span></h2>
        </div>
        
        <div class="card">
            <div class="card-decoration"></div>
            <div class="card-decoration"></div>
            
            <div class="card-content">
                <h1>Registro de Turno</h1>
                <p class="subtitle">Ingresa tu nombre para unirte a la fila virtual</p>
                
                <form method="POST" id="registro-form">
                    <div class="form-group">
                        <label for="nombre">Nombre completo</label>
                        <div class="input-wrapper">
                            <span class="input-icon">
                                <span class="user-icon"></span>
                            </span>
                            <input type="text" name="nombre" id="nombre" placeholder="Ingresa tu nombre" required>
                        </div>
                    </div>
                    
                    <button type="submit">Registrarse</button>
                </form>
                
                {% if mensaje %}
                <div class="success-message">
                    <div class="success-icon">
                        <span class="check-icon"></span>
                    </div>
                    <div>{{ mensaje }}</div>
                </div>
                {% endif %}
            </div>
        </div>
    </div>

    <script>
        // Add some simple animations and interactions
        const form = document.getElementById('registro-form');
        const input = document.getElementById('nombre');
        
        // Simple form validation feedback
        form.addEventListener('submit', (e) => {
            if (input.value.trim() === '') {
                e.preventDefault();
                input.style.borderColor = '#e74c3c';
                setTimeout(() => {
                    input.style.borderColor = '#e9ecef';
                }, 2000);
            } else {
                // Add a subtle button animation on valid submit
                const button = form.querySelector('button');
                button.innerHTML = 'Procesando...';
                button.style.opacity = '0.9';
            }
        });
        
        // Auto focus the input field on desktop, but not on mobile
        window.addEventListener('load', () => {
            // Only auto-focus on larger screens to avoid mobile keyboard popping up automatically
            if (window.innerWidth > 768) {
                setTimeout(() => {
                    input.focus();
                }, 500);
            }
        });
        
        // Fix for iOS height issues
        const viewportHeight = () => {
            let vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        };
        
        window.addEventListener('resize', viewportHeight);
        viewportHeight();
    </script>
</body>
</html>
"""

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if nombre:
            turnos_pendientes.append(nombre)
            mensaje = f"Turno generado para {nombre}"
        else:
            mensaje = "Nombre inválido"
    return render_template_string(formulario_html, mensaje=mensaje)

@app.route('/api/registro', methods=['POST'])
def api_registro():
    data = request.get_json()
    nombre = data.get('nombre')
    if nombre:
        turnos_pendientes.append(nombre)
        return jsonify({"mensaje": f"Turno generado para {nombre}"}), 200
    return jsonify({"error": "Nombre faltante"}), 400

@app.route('/api/turnos_pendientes', methods=['GET'])
def obtener_turnos():
    global turnos_pendientes
    pendientes = turnos_pendientes.copy()
    turnos_pendientes.clear()
    return jsonify(pendientes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

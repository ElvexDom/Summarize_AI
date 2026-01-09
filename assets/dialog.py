import time

def show_dialogYesNO(message_text, color="#4caf50"):
    """
    Génère un toast centré en bas pendant 2 secondes.
    """
    toast_html = f"""
    <div style="
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: {color};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
        font-family: Arial, sans-serif;
        text-align: center;
        opacity: 1;
        transition: opacity 0.5s ease-out;
        z-index: 9999;
        min-width: 250px;
    ">
        🎉 {message_text}
    </div>
    """
    yield toast_html
    time.sleep(2)
    yield ""
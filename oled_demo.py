from app.display import OledDisplay
from app.display_service import DisplayService

def main() -> None:
    # connect to the OLED Hardware
    display = OledDisplay()
    
    try:
        # giving display to the service
        service = DisplayService(display)
        
        # service will call render_text to render the text and then display it on the OLED
        service.show_text("Service active !!!")
        
        input("Press Enter to exit...")
    finally:
        display.close()
    

if __name__ == "__main__":
    main()  
    
        
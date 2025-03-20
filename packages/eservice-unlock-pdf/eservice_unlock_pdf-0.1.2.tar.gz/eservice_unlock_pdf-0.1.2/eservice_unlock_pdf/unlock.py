import pikepdf

def unlock_pdf(input_pdf, output_pdf, password):
    try:
        pdf = pikepdf.open(input_pdf, password=password)
        pdf.save(output_pdf)
        print(f"✅ PDF ปลดล็อกสำเร็จ! บันทึกที่: {output_pdf}")
        return True
    except pikepdf.PasswordError:  # เช็คกรณีรหัสผ่านผิด
        print("❌ รหัสผ่านไม่ถูกต้อง")
        return False
    except Exception as e:  # เช็ค Error อื่น ๆ เช่น ไฟล์ไม่พบ หรือไฟล์ไม่ใช่ PDF
        print(f"⚠️ Error: {e}")
        return False
# my_module.py
def my_function():
    print("กำลังรัน my_function")


# โค้ดส่วนนี้จะทำงานก็ต่อเมื่อไฟล์ถูกรันโดยตรง
# จะไม่ทำงานเมื่อถูก import
if __name__ == "__main__":
    print("ไฟล์นี้กำลังถูกรันเป็นสคริปต์")
    my_function()

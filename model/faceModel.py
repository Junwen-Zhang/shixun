import face_recognition
from fastapi import UploadFile,File
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
import shutil

class FaceModel():
    def __init__(self):
        return

    def face_comparison(self,file_to, file_standard):
        # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
        try:
            code1 = face_recognition.face_encodings(face_recognition.load_image_file(file_to))[0]
            # Load the uploaded image file
            code2 = face_recognition.face_encodings(face_recognition.load_image_file(file_standard))[0]
            face_found = False
            is_same_person = False
        #首先判断两张图片里有有人脸，然后再将这两张图片的人脸进行比对
            if len(code1) > 0 and len(code2) > 0:
                face_found = True           
                # See if the first face in the uploaded image matches the known face of Obama
                #判断第一个人脸是否匹配第二个人脸-------------------------------------------------------
                match_results = face_recognition.compare_faces([code1], code2)
                if match_results[0]:
                    is_same_person = True
        except Exception as e:
            print("人脸识别过程出错",e)
            # Return the result as json
        #注意这里不是并列的-------------------------------------------- 
        result = {
                "face_found_in_image": face_found,
                "is_same_person": is_same_person
            }

        return result
    def face_detect(self,facephoto):
        facephoto = face_recognition.load_image_file(facephoto)           ###还是必须load一下？？？！！！！这句话一定要有
        #使用默认模型，cnn模型太慢了
        face_locations = face_locations = face_recognition.face_locations(facephoto)
        number = len(face_locations)
        return number

if __name__=="__main__": 
    #以读的方式、且二进制打开  怎么将现有的文件变成文件流可以进行操作
    f1 = open('./pictures/1.jpeg', 'rb')
    f2 = open('./pictures/2.png','rb')

    facemodel = FaceModel()
    result = facemodel.face_comparison(f1,f2)
    print(result)

    facemodel.face_detect("./pictures/4.jpg")

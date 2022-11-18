from flask import Flask, render_template, request, redirect, g, send_file
from werkzeug.utils import secure_filename
import sys, os, glob
import extractAttributes

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('main.html')

@app.route('/file_upload', methods = ['GET', 'POST'])
def file_upload():
    # 기존 파일 삭제
    for file in os.scandir(f'.{os.path.sep}downloadedFile'):
        os.remove(file.path)
    for file in os.scandir(f'.{os.path.sep}out'):
        os.remove(file.path)

    if request.method == 'POST':
        f = request.files['file']

        # file extension check
        if secure_filename(f.filename).endswith(".docx") == False:
            return render_template('main.html', error = "docx 파일만 업로드 가능합니다.")

        f.save(f'downloadedFile{os.path.sep}' + secure_filename(f.filename))
        return redirect('/process/' + secure_filename(f.filename))
    else: 
        return redirect('/')
 
# 파일명 받아서 처리하는 페이지
@app.route('/process/<filename>')
def process(filename):
    outDirectory = f'.{os.path.sep}out'
    csvOut = False
    documents = [f'.{os.path.sep}downloadedFile{os.path.sep}' + filename]
    attributes, attributesSN = extractAttributes.processDocuments(documents, outDirectory, csvOut)
    # TODO csv나 dup 옵션 받아서 처리
    # if not attributes:
    #     exit(1)
    # if args.list or args.listDuplicates:
    #     printAttributeTables(attributes, attributesSN, args.listDuplicates)
    #     if args.csvOut:
    #         printAttributeCsv(attributes, args.outDirectory)
    #         if args.listDuplicates:
    #             printDuplicateCsv(attributes, attributesSN, args.outDirectory)
    return redirect('/download/' + filename)    

@app.route('/download/<filename>')
def Download_File(filename):
    PATH=f'.{os.path.sep}out{os.path.sep}' + 'attributes.json'
    # TODO 파일 전송하면서 완료 메시지 띄우기
    render_template('main.html', complete = "파일 다운로드 완료")
    return send_file(PATH, as_attachment=True)
		
if __name__ == '__main__':
    app.run(debug = True)
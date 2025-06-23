from fastapi import HTTPException, status
from fastapi import APIRouter, UploadFile, Depends
from . import schemas, models,service, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/upload_data",
    tags= ["upload"]
)

@router.post("/")
async def add_data(data:UploadFile, request:schemas.UploadData= Depends(),db: Session = Depends(database.get_db)):

    #validate file
    service.validate_file_extension(data.filename)
    raw_data = await data.read()
    service.validate_file_size(raw_data)

    #file storage
    upload_dir = service.create_upload_dir()
    safe_filename = service.check_filename(request.file_name)
    file_path = upload_dir / safe_filename
    if file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File with this name already exists"
        )

    with open (file_path , "wb" )as file:
        file.write(raw_data)

    #chunk data that is uploaded
    decoded_content = raw_data.decode("utf-8")
    split_docs = service.chunk_text(decoded_content )
    chunk_texts = [doc.page_content for doc in split_docs]
    embeddings = service.embeddings_model.embed_documents(chunk_texts)

    new_data = models.UploadedFile(file_name= request.file_name,
                                   file_type = request.file_type,
                                   description = request.description)
    db.add(new_data)
    db.flush()

    chunks =service.save_chunks(split_docs,embeddings,new_data.id)
    db.add_all(chunks)
    db.commit()
    return {
            "message": "File uploaded and processed successfully",
            "file_id": new_data.id,
            "chunks_created": len(chunks),
            "embedding_model": "all-MiniLM-L6-v2"
        }



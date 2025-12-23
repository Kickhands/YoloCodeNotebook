import cv2
import os

video_path = "C:\\Skripsi\\YoloCodeNotebook\\HandsignOnetoFive\\videorecord-rock-paper-scissor\\rockpaperscissor.mp4"
output_folder = "C:\\Skripsi\\YoloCodeNotebook\\HandsignOnetoFive\\frame-rock-paper-scissor"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Tidak bisa membuka video.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps

print(f"Frame rate video: {fps:.2f} FPS")
print(f"Total frame asli: {total_frames}")
print(f"Durasi video: {duration:.2f} detik ({duration/60:.2f} menit)")

saved_count = 0
frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Ubah angka 2 ini untuk kontrol jumlah frame:
    # 1 = ambil semua frame (paling banyak)
    # 2 = ambil setiap 2 frame sekali (setengah dari total)
    # 3 = setiap 3 frame sekali, dst.
    if frame_count % 4 == 0:  # <-- ubah angka 1 ini
        
        # Nama file unik berdasarkan urutan sebenarnya
        frame_filename = os.path.join(output_folder, f"frame_{saved_count:06d}.jpg")
        cv2.imwrite(frame_filename, frame)
        saved_count += 1
    
    frame_count += 1

cap.release()
print(f"Ekstraksi selesai! Total {saved_count} frame disimpan dari {frame_count} frame asli.")
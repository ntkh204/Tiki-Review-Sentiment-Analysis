**Sơ lược giải pháp**

Giải pháp của mình tập trung vào data hơn mô hình. Với bài toán này, mình tập trung tiền xử lý dữ liệu, loại bỏ nhiễu, gán nhãn lại các mislabel data. Lý do tập trung vào data hơn vì mình quan sát dữ liệu thấy có khá nhiều nhiễu, gán nhãn sai và lấy từ các trang thương mại điện tử nên từ ngữ lộn xộn, thường không theo văn phong chuẩn mực, cần phải có bước chuẩn hóa. Mô hình mình sử dụng là SVM và feature quen thuộc TF-IDF (5-gram). Lý do sử dụng SVM vì mình thấy SVM khá phù hợp với các bài toán có ít dữ liệu nhưng nhiều features. Cuối cùng là giải thích về việc dùng Error Analysis để gán lại các Mislabel data.

**Chi tiết cách thực hiện**

1. Tiền xử lý dữ liệu
Dữ liệu bình luận (văn nói) nên người dùng thường không quan tâm đến chữ hoa thường khi gõ, đưa hết về lower case.
Tiếng Việt có 2 cách bỏ dấu nên đưa về 1 chuẩn. Ví dụ, chữ "Hòa" và "Hoà" đều được chấp nhận trong tiếng Việt.
Loại bỏ emoji và emoticon
Gán nhãn tay toàn bộ data để tiến hành huấn luyện
Loại bỏ dấu câu (puntuations) và các ký tự nhiễu.
Xóa bỏ từ dừng
Chuyển các từ lóng (teencode) thành các từ chuẩn.
Tách từ để đảm bảo từ ghép không bị tách lẻ ra.
3. Lựa chọn mô hình/tunning
Mình chọn SVM, tunning một chút parameter. feature TF-IDF, 5 gram.
4. Sử dụng Error Analysis để gán lại nhãn
Bằng cách train 2 lần: Lần 1 chia tập train/test theo tỉ lệ 7/3 và lần 2 train overfitting, mình phát hiện ra các trường hợp gán nhãn sai và gán lại nhãn, lặp đi lặp lại quá trình này vài chục lần mình đã gán nhãn lại được khá nhiều data. Cách làm của mình dựa trên ý tưởng của Overfitting, nếu đã dạy mô hình tập dữ liệu A rồi test trên chính tập A đó mà mô hình chỉ đạt độ chính xác thấp chứng tỏ dữ liệu chưa phổ quát, quá ít dữ liệu hoặc gán nhãn sai. VD: Train 7/3 đạt 89%, train overfit đạt chỉ 94% thì chứng tỏ có nhiều data gán nhãn sai. Mình gán lại nhãn đến khi độ chính xác khi train overfit đạt khoảng 99% thì dừng lại, lúc này độ chính xác của train 7/3 đạt khoảng 94%. Việc gán lại nhãn, loại bỏ nhiễu với train data là một phần của data science và hoàn toàn hợp lệ. (Tất nhiên là không động chút nào đến test data).

**Kết quả**

Mình chạy Crossvalidation 5 folds để đánh giá model công bằng hơn. Kết quả cuối cùng CV5fold với tập dữ liệu đã gán lại nhãn là 94.6%. 

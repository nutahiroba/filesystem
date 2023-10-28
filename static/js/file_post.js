
const textElements = document.querySelectorAll('text');

textElements.forEach((textElement) => {
    textElement.addEventListener('click', () => {
        const textContent = textElement.textContent;
        console.log(textContent);

        // テキストの内容をPOSTする
        fetch('/post_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: textContent }),
        })
        .then((response) => {
            if (response.ok) {
                console.log('テキストがPOSTされました');
            } else {
                console.error('テキストのPOSTに失敗しました');
            }
            return response.json();
        })
        .then(data => {
          // レスポンスからファイルリストを取得して表示
          const fileList = data.items;
          fileList.unshift('ファイル名');
          const tableBody = document.querySelector('table tbody');
          tableBody.innerHTML = ''; // 現在のテーブル内容をクリア

          fileList.forEach((item) => {
              const row = document.createElement('tr');
              const cell = document.createElement('td');
              cell.textContent = item;
              row.appendChild(cell);
              tableBody.appendChild(row);
          });
        })
        .catch((error) => {
            console.error('エラー: ' + error);
        });
    });
});
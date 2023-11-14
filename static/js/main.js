document
  .getElementById("generateForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    var formData = new FormData(this);

    fetch("/generate", {
      // ここにはサーバーのエンドポイントURLを入れてください
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // ここでレスポンスデータを処理します
        console.log(data);
        const wc = data.items;
        const wcdisplay = document.getElementById("wordcloud");

        wcdisplay.innerHTML = wc;

        const recordedTexts = [];

        const textElements = document.querySelectorAll("text");

        textElements.forEach((textElement) => {
          // ------------------transform属性をx,y属性に変更する----------------------

          // transform属性の値を取得
          const transformValue = textElement.getAttribute("transform");

          // 正規表現を使用してxとyの値を抽出
          const regex = /translate\((\d+),(\d+)\)/;
          const match = transformValue.match(regex);

          if (match) {
            const x = match[1];
            const y = match[2];

            // xとyの属性を設定
            textElement.setAttribute("x", x);
            textElement.setAttribute("y", y);

            // transform属性を削除
            textElement.removeAttribute("transform");
          }

          const textContent = textElement.textContent;

          // IDとして適切な形式に変換（空白をアンダースコアに、特殊文字を削除）
          // console.log(textContent);
          // let validId = textContent.replace(/\s+/g, "_").replace(/\W+/g, "");

          // text要素にIDを設定
          textElement.setAttribute("id", textContent);
          // ------------------以下クリック時----------------------

          textElement.addEventListener("click", () => {
            const clickedText = textElement.textContent;

            const index = recordedTexts.indexOf(clickedText);

            // ------------------クリック時に枠を追加----------------------
            if (index === -1) {
              // リストに格納
              recordedTexts.push(clickedText);

              // // 枠の要素を作成
              // const bbox = textElement.getBBox();
              // const rect = document.createElementNS(
              //   "http://www.w3.org/2000/svg",
              //   "rect"
              // );
              // rect.setAttribute("x", bbox.x);
              // rect.setAttribute("y", bbox.y);
              // rect.setAttribute("width", bbox.width);
              // rect.setAttribute("height", bbox.height);
              // rect.setAttribute("stroke", "red");
              // rect.setAttribute("fill", "transparent");
              // rect.setAttribute("stroke-width", "3");
              // rect.setAttribute("class", "outlined");
              // // 枠をSVGに追加
              // textElement.parentNode.insertBefore(rect, textElement);

              // ------------------クリック時に枠を削除----------------------
            } else {
              // リストから削除
              recordedTexts.splice(index, 1);

              // 枠を削除
              // const outlinedRect = document.querySelector(".outlined");
              // if (outlinedRect) {
              //   outlinedRect.parentNode.removeChild(outlinedRect);
              // }
            }

            // SVG要素内の全てのrect要素を選択し、削除
            document
              .querySelectorAll("svg rect")
              .forEach((rect) => rect.remove());

            recordedTexts.forEach((text) => {
              const textElement = document.getElementById(text);
              // 枠の要素を作成
              const bbox = textElement.getBBox();
              const rect = document.createElementNS(
                "http://www.w3.org/2000/svg",
                "rect"
              );
              rect.setAttribute("x", bbox.x);
              rect.setAttribute("y", bbox.y);
              rect.setAttribute("width", bbox.width);
              rect.setAttribute("height", bbox.height);
              rect.setAttribute("stroke", "red");
              rect.setAttribute("fill", "transparent");
              rect.setAttribute("stroke-width", "3");
              rect.setAttribute("class", "outlined");
              // 枠をSVGに追加
              textElement.parentNode.insertBefore(rect, textElement);
            });

            console.log(recordedTexts);

            fetch("/sendList", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ recordedTexts: recordedTexts }),
            })
              .then((response) => {
                if (response.ok) {
                  console.log("テキストがPOSTされました");
                } else {
                  console.error("テキストのPOSTに失敗しました");
                }
                return response.json();
              })
              // -------------------------受け取った値の処理--------------------------
              .then((data) => {
                const fileList = data.items;
                console.log(fileList);
                const filecount = document.getElementById("file_count");
                filecount.textContent = fileList.length + "件";

                const filedisplay = document.getElementById("file_list");
                filedisplay.innerHTML = "";
                if (fileList == "undified") {
                  filedisplay.innerHTML = "<p>対象無し</p>";
                } else {
                  fileList.unshift("ファイル名");
                  fileList.forEach((item) => {
                    const row = document.createElement("tr");
                    const cell = document.createElement("td");
                    cell.textContent = item.split("\\").pop();
                    row.appendChild(cell);
                    filedisplay.appendChild(row);
                  });
                }
              })
              .catch((error) => {
                console.log("エラー" + error);
              });
          });
        });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

// スライダーの値を表示する関数
function updateSliderValue(sliderId, displayId) {
  var slider = document.getElementById(sliderId);
  var display = document.getElementById(displayId);
  display.textContent = slider.value;
  slider.oninput = function () {
    display.textContent = this.value;
  };
}

// 各スライダーの値の更新を設定
updateSliderValue("height", "heightVal");
updateSliderValue("width", "widthVal");
updateSliderValue("min", "minVal");
updateSliderValue("max", "maxVal");
updateSliderValue("step", "stepVal");

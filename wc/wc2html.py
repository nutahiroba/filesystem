def get(wc, file_path):
  link_script = """
<script>

// SVG要素を取得
const svg = document.querySelector('svg');

// 全てのtext要素を取得
const textElements = svg.querySelectorAll('text');

// 各text要素に対して処理
textElements.forEach(textElement => {
    // transform属性の値を取得
    const transformValue = textElement.getAttribute('transform');

    // 正規表現を使用してxとyの値を抽出
    const regex = /translate\((\d+),(\d+)\)/;
    const match = transformValue.match(regex);

    if (match) {
        const x = match[1];
        const y = match[2];

        // xとyの属性を設定
        textElement.setAttribute('x', x);
        textElement.setAttribute('y', y);

        // transform属性を削除
        textElement.removeAttribute('transform');
    }
});

document.querySelectorAll('text').forEach(textElement => {
  let textClicked = false;

  // テキスト要素をクリックしたときの処理
  textElement.addEventListener('click', () => {
    if (!textClicked) {
    const position = textElement.getAttribute('transform');
        // 枠の要素を作成
        const bbox = textElement.getBBox();
        const rect = document.createElementNS("http://www.w3.org/2000/svg", 'rect');
        rect.setAttribute('x', bbox.x);
        rect.setAttribute('y', bbox.y);
        rect.setAttribute('width', bbox.width);
        rect.setAttribute('height', bbox.height);
        rect.setAttribute('stroke', 'red'); // 枠の色を黒に設定
        rect.setAttribute('fill', 'transparent');
        rect.setAttribute('stroke-width', '3');
        rect.setAttribute('class', 'outlined');
  
        // 枠をSVGに追加
        textElement.parentNode.insertBefore(rect, textElement);

      textClicked = true;
    } else {
      // 枠を削除
      const outlinedRect = document.querySelector('.outlined');
      if (outlinedRect) {
        outlinedRect.parentNode.removeChild(outlinedRect);
      }

      textClicked = false;
    }
  });
});
</script>"""

  html_script = """
  <!DOCTYPE html>\n
  """

  # HTMLファイルに書き出し
  with open(file_path, "w", encoding ="utf-8") as f:
      f.write(html_script)
      f.write(wc.to_svg())
      f.write(link_script)
      
  return 0
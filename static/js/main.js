const recordedTexts = [];

const textElements = document.querySelectorAll('text');

textElements.forEach(textElement => {
	// ------------------transform属性をx,y属性に変更する----------------------

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

	const textContent = textElement.textContent;

	// ------------------以下クリック時----------------------

	textElement.addEventListener('click', () => {
		const  clickedText = textElement.textContent;

		const index = recordedTexts.indexOf(clickedText);

		// ------------------クリック時に枠を追加----------------------
		if (index === -1) {
			// リストに格納
			recordedTexts.push(clickedText);

			// 枠の要素を作成
			const bbox = textElement.getBBox();
			const rect = document.createElementNS("http://www.w3.org/2000/svg", 'rect');
			rect.setAttribute('x', bbox.x);
			rect.setAttribute('y', bbox.y);
			rect.setAttribute('width', bbox.width);
			rect.setAttribute('height', bbox.height);
			rect.setAttribute('stroke', 'red'); 
			rect.setAttribute('fill', 'transparent');
			rect.setAttribute('stroke-width', '3');
			rect.setAttribute('class', 'outlined');
			console.log(textElement);
			// 枠をSVGに追加
			textElement.parentNode.insertBefore(rect, textElement);

		// ------------------クリック時に枠を削除----------------------
		} else {
			// リストから削除
			recordedTexts.splice(index, 1);

			// 枠を削除
			const outlinedRect = document.querySelector('.outlined');
			if (outlinedRect) {
				outlinedRect.parentNode.removeChild(outlinedRect);
			}
		}
	console.log(recordedTexts);
	})
})
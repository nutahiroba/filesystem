def get(wc):
  link_script = """
  <script>
    svg = document.getElementsByTagName("svg")[0];
    text_tags =  svg.getElementsByTagName("text")
    for(var i=0; i<text_tags.length; i++){
        text_tags[i].addEventListener(
            "click",
            function(){
                word = this.textContent;
                console.log(this);
                this.setAttribute("style", "border: 3px solid;");
                word_uri = encodeURI(word);
                url = "https://www.google.com/search?q=" + word_uri;
                window.open(url, "_bkank");

            }
        )
    }
  </script>"""

  html_script = """
  <!DOCTYPE html>\n
  """

  # HTMLファイルに書き出し
  with open("wc.html", "w", encoding ="utf-8") as f:
      f.write(html_script)
      f.write(wc.to_svg())
      f.write(link_script)
      
  return 0
# DR Cos Projection Converter
converts pdfs from [dr-cos.info](https://dr-cos.info/) into projectable PDFs suitable for [patternprojector.com](https://www.patternprojector.com/)


we do this by 
- cropping the PDF by the overlap border of the original (using fritz)
- killing the `userunit` using ghostscript
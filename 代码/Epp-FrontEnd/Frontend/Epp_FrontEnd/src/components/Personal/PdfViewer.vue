<template>
  <div>
    <canvas ref="pdfViewer"></canvas>
  </div>
</template>

<script>
import pdfjsLib from 'pdfjs-dist'

export default {
  mounted () {
    const { reportId } = this.$route.params

    pdfjsLib.getDocument(`/path/to/pdf/${reportId}.pdf`).promise.then((pdf) => {
      pdf.getPage(1).then((page) => {
        const canvas = this.$refs.pdfViewer
        const context = canvas.getContext('2d')
        const viewport = page.getViewport({ scale: 1.5 })

        canvas.height = viewport.height
        canvas.width = viewport.width

        const renderContext = {
          canvasContext: context,
          viewport: viewport
        }

        page.render(renderContext)
      })
    })
  }
}
</script>

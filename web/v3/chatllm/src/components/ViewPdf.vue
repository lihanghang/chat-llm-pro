<template>
<div>
  <iframe height="100%" width=100% :src="`${getFilePath}`" ></iframe>
</div>
</template>

<script>
export default defineComponent({
  name: 'Home'
  components: { ViewPdf }
  setup() {
    const pdfSrc = '/Users/memect/Downloads/基于RoBERTa的全局图神经网络文档级中文金融事件抽取.pdf'
    const numOfPages = ref(0)

    onMounted(() => {
      const loadingTask = createLoadingTask(pdfSrc.value)
      loadingTask.promise.then((pdf: PDFDocumentProxy) => {
        numOfPages.value = pdf.numPages
      })
    })
    return {
      pdfSrc,
      numOfPages
    }
  }
});
</script>
<style scoped>
div {
  width: 50%;
  height: 79vh;
  min-width: 400px;
}
</style>
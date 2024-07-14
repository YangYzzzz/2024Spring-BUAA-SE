<template>
    <div>
        <el-input v-model="text" placeholder="请输入回复" @keyup.enter.native="submit"></el-input>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                text: "",
            }
        },
        methods: {
            submit() {
                this.$emit('submit', this.text)
                this.text = ""
            }
        },
    }
</script>

<style>

</style>
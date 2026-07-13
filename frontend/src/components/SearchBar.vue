<template>
    <div class="input-group">
        <input v-model="search" class="form-control" placeholder="Search..." @keyup.enter="emitSearch">
        <button class="btn btn-primary" @click="emitSearch">
            Search
        </button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            search: ""
        }
    },
    methods: {
        emitSearch() {
            this.$emit("search", this.search)
        }
    }
}
</script>
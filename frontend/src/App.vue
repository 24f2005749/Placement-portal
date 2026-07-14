<template>
    <router-view />
    <ToastHost />
</template>

<script>
import ToastHost from "@/components/ToastHost.vue"

export default {
    components: {
        ToastHost
    }
}
</script>

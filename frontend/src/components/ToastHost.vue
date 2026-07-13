<template>
    <div class="toast-container position-fixed top-0 end-0 p-3">
        <div v-for="toast in toasts" :key="toast.id" class="toast show border-0 shadow" :class="toastClass(toast.type)"
            role="status">
            <div class="d-flex">
                <div class="toast-body">
                    {{ toast.message }}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" aria-label="Close"
                    @click="remove(toast.id)"></button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            toasts: []
        }
    },

    mounted() {
        window.addEventListener("app-toast", this.add)
    },

    beforeUnmount() {
        window.removeEventListener("app-toast", this.add)
    },

    methods: {
        add(event) {
            const toast = {
                id: Date.now() + Math.random(),
                type: event.detail?.type || "info",
                message: event.detail?.message || "Done"
            }

            this.toasts.push(toast)

            setTimeout(() => this.remove(toast.id), 3500)
        },

        remove(id) {
            this.toasts = this.toasts.filter(toast => toast.id !== id)
        },

        toastClass(type) {
            if (type === "success") return "text-bg-success"
            if (type === "danger") return "text-bg-danger"
            if (type === "warning") return "text-bg-warning"
            return "text-bg-primary"
        }
    }
}
</script>

<template>
    <span class="badge status-badge" :class="color">
        {{ status }}
    </span>
</template>

<script>
export default {
    props: ["status"],
    computed: {
        color() {
            if (this.status == "approved")
                return "bg-success"

            if (this.status == "pending")
                return "bg-warning"

            if (this.status == "rejected")
                return "bg-danger"

            if (this.status == "selected")
                return "bg-success"

            if (this.status == "shortlisted")
                return "bg-primary"

            if (this.status == "open")
                return "bg-info"

            if (this.status == "closed")
                return "bg-secondary"

            return "bg-secondary"

        }
    }
}

</script>

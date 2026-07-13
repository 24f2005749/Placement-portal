<template>
    <DashboardLayout>
        <PageTitle title="Applications" />
        <Loader v-if="loading" />
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
        <EmptyState v-else-if="applications.length == 0" message="No applications found" />
        <ApplicationCard v-else v-for="application in applications" :key="application.application_id"
            :application="application" />
    </DashboardLayout>
</template>
<script>
import api from "@/services/api"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import ApplicationCard from "@/components/ApplicationCard.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"
export default {
    components: {
        DashboardLayout,
        PageTitle,
        ApplicationCard,
        Loader,
        EmptyState
    },
    data() {
        return {
            applications: [],
            loading: true,
            error: ""
        }
    },
    async mounted() {
        await this.fetchApplications()
    },
    methods: {
        async fetchApplications() {
            this.loading = true
            this.error = ""
            try {
                const response = await api.get("/admin/applications")
                this.applications = response.data
            }
            catch (error) {
                this.error = error.response?.data?.message || "Failed to load applications"
                console.error(error)
            }
            finally {
                this.loading = false
            }
        }
    }
}
</script>
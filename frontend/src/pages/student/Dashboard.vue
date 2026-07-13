<template>

    <DashboardLayout>

        <PageTitle title="Student Dashboard" />

        <div class="d-flex justify-content-end mb-3">
            <button class="btn btn-outline-primary" :disabled="exporting" @click="exportApplications">
                {{ exporting ? "Exporting..." : "Export Applications CSV" }}
            </button>
        </div>

        <div class="row g-3">

            <div class="col-md-3">

                <StatCard title="Available Drives" :value="stats.drives" />

            </div>

            <div class="col-md-3">

                <StatCard title="Applications" :value="stats.applications" />

            </div>

            <div class="col-md-3">

                <StatCard title="Selected" :value="stats.selected" />

            </div>

            <div class="col-md-3">

                <StatCard title="Pending" :value="stats.pending" />

            </div>

        </div>

        <div class="mt-5">

            <h4>

                Recent Applications

            </h4>

            <Loader v-if="loading" />

            <EmptyState v-else-if="applications.length == 0" message="No applications yet" />

            <ApplicationCard v-else v-for="application in applications" :key="application.application_id"
                :application="application" />

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>

        </div>

    </DashboardLayout>

</template>

<script>

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import StatCard from "@/components/StatCard.vue"
import ApplicationCard from "@/components/ApplicationCard.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"
import api from "@/services/api"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        StatCard,
        ApplicationCard,
        Loader,
        EmptyState
    },

    data() {

        return {

            stats: {
                drives: 0,
                applications: 0,
                selected: 0,
                pending: 0
            },

            applications: [],
            loading: true,
            error: "",
            exporting: false,
            exportJobId: null

        }

    },

    async mounted() {

        await this.loadData()

    },

    methods: {

        async loadData() {

            this.loading = true
            this.error = ""

            try {

                const applicationsResponse = await api.get("/student/applications")

                this.applications = applicationsResponse.data

                this.stats.applications = applicationsResponse.data.length

                this.stats.selected = applicationsResponse.data.filter(
                    x => x.status == "selected"
                ).length

                this.stats.pending = applicationsResponse.data.filter(
                    x => x.status == "applied"
                ).length

                const drivesResponse = await api.get("/student/drives")

                this.stats.drives = drivesResponse.data.length

            }

            catch (error) {

                this.error = error.response?.data?.message || "Failed to load dashboard"

                console.error(error)

            }

            finally {

                this.loading = false

            }

        },

        async exportApplications() {

            this.exporting = true
            this.error = ""

            try {

                const response = await api.post("/student/applications/export")
                this.exportJobId = response.data.job_id
                this.pollExport()

            }

            catch (error) {

                this.exporting = false
                this.error = error.response?.data?.message || "Failed to start export"

            }

        },

        async pollExport() {

            if (!this.exportJobId) return

            try {

                const response = await api.get("/jobs/" + this.exportJobId)

                if (response.data.state === "SUCCESS") {
                    await this.downloadExport(response.data.result?.filename)
                    this.exporting = false
                    this.exportJobId = null
                    alert("Applications CSV export completed.")
                    return
                }

                if (response.data.state === "FAILURE") {
                    this.exporting = false
                    this.error = response.data.message || "Export failed"
                    return
                }

                setTimeout(this.pollExport, 2000)

            }

            catch (error) {

                this.exporting = false
                this.error = error.response?.data?.message || "Failed to check export status"

            }

        },

        async downloadExport(filename) {

            if (!filename) return

            const response = await api.get("/student/applications/export/" + filename, {
                responseType: "blob"
            })

            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement("a")
            link.href = url
            link.setAttribute("download", filename)
            document.body.appendChild(link)
            link.click()
            link.remove()
            window.URL.revokeObjectURL(url)

        }

    }

}

</script>

<template>

    <DashboardLayout>

        <PageTitle title="Company Dashboard" />

        <div class="row g-3">

            <div class="col-md-4">

                <StatCard title="My Drives" :value="stats.drives" />

            </div>

            <div class="col-md-4">

                <StatCard title="Applicants" :value="stats.applicants" />

            </div>

            <div class="col-md-4">

                <StatCard title="Pending Drives" :value="stats.pending" />

            </div>

        </div>

        <div class="mt-5">

            <div class="d-flex justify-content-between align-items-center">
                <h4>Recent Drives</h4>
                <router-link class="btn btn-sm btn-outline-primary" to="/company/drives">View All</router-link>
            </div>

            <Loader v-if="loading" />

            <EmptyState v-else-if="drives.length == 0" message="No drives created yet." />

            <DriveCard v-else v-for="drive in drives" :key="drive.id" :drive="drive" @view="viewDrive" />

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>

        </div>

    </DashboardLayout>

</template>

<script>

import api from "@/services/api"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import StatCard from "@/components/StatCard.vue"
import Loader from "@/components/Loader.vue"
import DriveCard from "@/components/DriveCard.vue"
import EmptyState from "@/components/EmptyState.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        StatCard,
        Loader,
        DriveCard,
        EmptyState
    },

    data() {

        return {

            stats: {
                drives: 0,
                applicants: 0,
                pending: 0
            },
            drives: [],
            loading: true,
            error: ""

        }

    },

    async mounted() {

        await this.loadDashboard()

    },

    methods: {

        async loadDashboard() {

            this.loading = true
            this.error = ""

            try {

                const response = await api.get("/company/dashboard")
                const drivesResponse = await api.get("/company/drives")

                this.stats = response.data
                this.drives = drivesResponse.data.slice(0, 3)

            }

            catch (error) {

                this.error = error.response?.data?.message || "Failed to load dashboard"

                console.error(error)

            }

            finally {

                this.loading = false

            }

        },

        viewDrive(id) {
            this.$router.push("/company/drives/" + id)
        }

    }

}



</script>

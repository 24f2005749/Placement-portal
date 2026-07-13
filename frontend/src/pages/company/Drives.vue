<template>

    <DashboardLayout>

        <PageTitle title="My Drives" />

        <div class="d-flex justify-content-end mb-3">

            <button class="btn btn-success" @click="$router.push('/company/drives/create')">

                Create Drive

            </button>

        </div>

        <Loader v-if="loading" />

        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

        <EmptyState v-else-if="drives.length == 0" message="No drives created yet." />

        <DriveCard v-else v-for="drive in drives" :key="drive.id" :drive="drive" @view="viewDrive" />

    </DashboardLayout>

</template>

<script>

import api from "@/services/api"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"
import DriveCard from "@/components/DriveCard.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        Loader,
        EmptyState,
        DriveCard
    },

    data() {

        return {

            drives: [],
            loading: true,
            error: ""

        }

    },

    async mounted() {

        await this.fetchDrives()

    },

    methods: {

        async fetchDrives() {
            this.loading = true
            this.error = ""

            try {
                const response = await api.get("/company/drives")
                this.drives = response.data
            }
            catch (error) {
                this.error = error.response?.data?.message || "Failed to load drives"
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

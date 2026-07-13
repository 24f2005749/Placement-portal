<template>

    <DashboardLayout>

        <PageTitle title="My Applications" />

        <Loader v-if="loading" />

        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

        <EmptyState v-else-if="applications.length == 0" message="You haven't applied to any drives yet." />

        <div v-else>

            <ApplicationCard v-for="application in applications" :key="application.application_id"
                :application="application" />

        </div>

    </DashboardLayout>

</template>

<script>

import api from "@/services/api"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"
import ApplicationCard from "@/components/ApplicationCard.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        Loader,
        EmptyState,
        ApplicationCard
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

                const response = await api.get("/student/applications")

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
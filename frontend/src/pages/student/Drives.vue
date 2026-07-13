<template>

    <DashboardLayout>

        <PageTitle title="Available Drives" />

        <SearchBar @search="searchDrives" />

        <div class="mt-3">
            <select v-model="eligibilityFilter" class="form-select" @change="applyFilters">
                <option value="all">All drives</option>
                <option value="eligible">Eligible for me</option>
                <option value="not_eligible">Not eligible</option>
            </select>
        </div>

        <div class="mt-4">

            <Loader v-if="loading" />

            <EmptyState v-else-if="drives.length == 0" message="No Drives Found" />

            <DriveCard v-else v-for="drive in drives" :key="drive.id" :drive="drive" @view="viewDrive" />

        </div>

    </DashboardLayout>

</template>

<script>

import api from "@/services/api"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import SearchBar from "@/components/SearchBar.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"
import DriveCard from "@/components/DriveCard.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        SearchBar,
        Loader,
        EmptyState,
        DriveCard
    },

    data() {

        return {

            drives: [],
            allDrives: [],
            loading: true,
            searchText: "",
            eligibilityFilter: "all"

        }

    },

    async mounted() {

        await this.fetchDrives()

    },

    methods: {

        async fetchDrives(query = "") {

            this.loading = true

            try {

                const response = await api.get("/student/drives", {
                    params: query.trim() ? { q: query } : {}
                })

                this.drives = response.data
                this.allDrives = response.data

            }

            catch (error) {

                alert(error.response?.data?.message || "Failed to load drives")

            }

            finally {

                this.loading = false

            }

        },

        async searchDrives(search) {

            this.searchText = search
            await this.fetchDrives(search)

        },

        applyFilters() {

            let filtered = this.allDrives

            const search = this.searchText.toLowerCase()

            if (search.trim()) {

                filtered = filtered.filter(drive =>

                    drive.title.toLowerCase().includes(search)
                    ||
                    drive.company_name.toLowerCase().includes(search)
                    ||
                    (drive.location || "").toLowerCase().includes(search)

                )

            }

            if (this.eligibilityFilter === "eligible") {
                filtered = filtered.filter(drive => drive.eligible === true)
            }

            if (this.eligibilityFilter === "not_eligible") {
                filtered = filtered.filter(drive => drive.eligible === false)
            }

            this.drives = filtered

        },

        viewDrive(id) {

            this.$router.push("/student/drives/" + id)

        }

    }

}

</script>

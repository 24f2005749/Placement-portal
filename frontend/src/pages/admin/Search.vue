<template>

    <DashboardLayout>

        <PageTitle title="Search" />

        <SearchBar @search="search" />

        <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>

        <Loader v-if="loading" class="mt-5" />

        <template v-else>

            <h4 class="mt-5">

                Students ({{ students.length }})

            </h4>

            <EmptyState v-if="searched && students.length == 0" message="No students found" />

            <StudentCard v-for="student in students" :key="student.id" :student="student" :show-actions="false" />

            <h4 class="mt-5">

                Companies ({{ companies.length }})

            </h4>

            <EmptyState v-if="searched && companies.length == 0" message="No companies found" />

            <CompanyCard v-for="company in companies" :key="company.id" :company="company" />

            <h4 class="mt-5">

                Drives ({{ drives.length }})

            </h4>

            <EmptyState v-if="searched && drives.length == 0" message="No drives found" />

            <DriveCard v-for="drive in drives" :key="drive.id" :drive="drive" :show-actions="false" />

        </template>

    </DashboardLayout>

</template>

<script>

import api from "@/services/api"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import SearchBar from "@/components/SearchBar.vue"
import StudentCard from "@/components/StudentCard.vue"
import CompanyCard from "@/components/CompanyCard.vue"
import DriveCard from "@/components/DriveCard.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        SearchBar,
        StudentCard,
        CompanyCard,
        DriveCard,
        Loader,
        EmptyState
    },

    data() {

        return {

            students: [],
            companies: [],
            drives: [],
            loading: false,
            error: "",
            searched: false

        }

    },

    methods: {

        async search(q) {

            if (!q.trim()) {

                this.students = []
                this.companies = []
                this.drives = []
                this.searched = false
                return

            }

            this.loading = true
            this.error = ""
            this.searched = true

            try {

                const response = await api.get("/admin/search", {
                    params: {
                        q
                    }
                })

                this.students = response.data.students

                this.companies = response.data.companies

                this.drives = response.data.drives

            }

            catch (error) {

                this.error = error.response?.data?.message || "Search failed"

                console.error(error)

            }

            finally {

                this.loading = false

            }

        }

    }

}

</script>

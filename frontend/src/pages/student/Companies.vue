<template>

    <DashboardLayout>

        <PageTitle title="Companies" />

        <SearchBar @search="searchCompanies" />

        <Loader v-if="loading" class="mt-4" />

        <div v-else-if="error" class="alert alert-danger mt-4">{{ error }}</div>

        <EmptyState v-else-if="companies.length === 0" message="No companies found" />

        <div v-else class="mt-4">

            <CompanyCard v-for="company in companies" :key="company.id" :company="company" />

        </div>

    </DashboardLayout>

</template>

<script>

import api from "@/services/api"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import SearchBar from "@/components/SearchBar.vue"
import CompanyCard from "@/components/CompanyCard.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        SearchBar,
        CompanyCard,
        Loader,
        EmptyState
    },

    data() {

        return {
            companies: [],
            loading: true,
            error: ""
        }

    },

    async mounted() {

        await this.fetchCompanies()

    },

    methods: {

        async fetchCompanies(query = "") {

            this.loading = true
            this.error = ""

            try {

                const response = await api.get("/student/companies", {
                    params: query.trim() ? { q: query } : {}
                })

                this.companies = response.data

            }

            catch (error) {

                this.error = error.response?.data?.message || "Failed to load companies"

            }

            finally {

                this.loading = false

            }

        },

        async searchCompanies(query) {

            await this.fetchCompanies(query)

        }

    }

}

</script>

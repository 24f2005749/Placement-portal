<template>
    <DashboardLayout>
        <PageTitle title="Company Approval" />

        <Loader v-if="loading" />
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
        <EmptyState
            v-else-if="pendingCompanies.length === 0"
            message="No companies are waiting for approval."
        />

        <DashboardTable v-else title="Pending Companies">
            <template #head>
                <th>Company</th>
                <th>HR</th>
                <th>Website</th>
                <th>Status</th>
                <th>Actions</th>
            </template>

            <template #body>
                <tr v-for="company in pendingCompanies" :key="company.id">
                    <td>{{ company.company_name }}</td>
                    <td>{{ company.hr_name || "Not provided" }}</td>
                    <td>
                        <a v-if="company.website" :href="company.website" target="_blank" rel="noreferrer">
                            Visit
                        </a>
                        <span v-else class="text-muted">Not provided</span>
                    </td>
                    <td><StatusBadge :status="company.approval_status" /></td>
                    <td>
                        <button class="btn btn-success btn-sm me-2" @click="updateCompany(company.id, 'approved')">
                            Approve
                        </button>
                        <button class="btn btn-outline-danger btn-sm" @click="updateCompany(company.id, 'rejected')">
                            Reject
                        </button>
                    </td>
                </tr>
            </template>
        </DashboardTable>
    </DashboardLayout>
</template>

<script>
import api from "@/services/api"
import { showToast } from "@/utils/toast"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DashboardTable from "@/components/DashboardTable.vue"
import PageTitle from "@/components/PageTitle.vue"
import StatusBadge from "@/components/StatusBadge.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"

export default {
    components: { DashboardLayout, DashboardTable, PageTitle, StatusBadge, Loader, EmptyState },

    data() {
        return {
            companies: [],
            loading: true,
            error: ""
        }
    },

    computed: {
        pendingCompanies() {
            return this.companies.filter(company => company.approval_status === "pending")
        }
    },

    async mounted() {
        await this.fetchCompanies()
    },

    methods: {
        async fetchCompanies() {
            this.loading = true
            this.error = ""

            try {
                const response = await api.get("/admin/companies")
                this.companies = response.data
            } catch (error) {
                this.error = error.response?.data?.message || "Failed to load companies"
            } finally {
                this.loading = false
            }
        },

        async updateCompany(id, approval_status) {
            try {
                await api.put(`/admin/companies/${id}`, { approval_status })
                showToast(`Company ${approval_status}`, "success")
                await this.fetchCompanies()
            } catch (error) {
                showToast(error.response?.data?.message || "Failed to update company", "danger")
            }
        }
    }
}
</script>

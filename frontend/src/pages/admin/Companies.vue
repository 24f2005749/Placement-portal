<template>

	<DashboardLayout>

		<PageTitle title="Companies" />

		<SearchBar @search="search" />

		<div class="mt-4">

			<Loader v-if="loading" />

			<div v-else-if="error" class="alert alert-danger">{{ error }}</div>

			<EmptyState v-else-if="companies.length == 0" message="No companies found" />

			<DashboardTable v-else title="Companies">
				<template #head>
					<th>Name</th>
					<th>HR</th>
					<th>Email</th>
					<th>Status</th>
					<th>Active</th>
					<th>Actions</th>
				</template>

				<template #body>
					<tr v-for="company in companies" :key="company.id">
						<td>{{ company.company_name }}</td>
						<td>{{ company.hr_name || "Not provided" }}</td>
						<td>{{ company.hr_email || "Not provided" }}</td>
						<td>
							<StatusBadge :status="company.approval_status" />
						</td>
						<td>{{ company.active ? "Yes" : "No" }}</td>
						<td>
							<button class="btn btn-success btn-sm me-2" @click="updateCompany(company.id, 'approved')"
								:disabled="company.approval_status == 'approved' || updatingId == company.id">
								{{ updatingId == company.id ? "Updating..." : "Approve" }}
							</button>
							<button class="btn btn-outline-danger btn-sm" @click="updateCompany(company.id, 'rejected')"
								:disabled="company.approval_status == 'rejected' || updatingId == company.id">
								Reject
							</button>
							<button class="btn btn-sm ms-2"
								:class="company.active ? 'btn-outline-warning' : 'btn-outline-success'"
								@click="toggleCompany(company)" :disabled="updatingId == company.id">
								{{ company.active ? "Deactivate" : "Activate" }}
							</button>
						</td>
					</tr>
				</template>
			</DashboardTable>

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
import DashboardTable from "@/components/DashboardTable.vue"
import StatusBadge from "@/components/StatusBadge.vue"
import { showToast } from "@/utils/toast"

export default {

	components: {
		DashboardLayout,
		PageTitle,
		SearchBar,
		Loader,
		EmptyState,
		DashboardTable,
		StatusBadge
	},

	data() {

		return {

			companies: [],
			allCompanies: [],
			loading: true,
			error: "",
			updatingId: null

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
				this.allCompanies = response.data

			}

			catch (error) {

				this.error = error.response?.data?.message || "Failed to load companies"

				console.error(error)

			}

			finally {

				this.loading = false

			}

		},

		async search(q) {

			if (!q.trim()) {

				this.companies = this.allCompanies
				return

			}

			this.companies = this.allCompanies.filter(company =>

				company.company_name.toLowerCase().includes(q.toLowerCase())

			)

		},

		async updateCompany(id, approval_status) {

			this.updatingId = id

			try {

				await api.put("/admin/companies/" + id, { approval_status })
				showToast("Company updated successfully", "success")
				await this.fetchCompanies()

			}

			catch (error) {

				showToast(error.response?.data?.message || "Failed to update company", "danger")

			}
			finally {
				this.updatingId = null
			}

		},

		async toggleCompany(company) {

			this.updatingId = company.id

			try {

				await api.put("/admin/companies/" + company.id, { approval_status: company.approval_status, active: !company.active })
				showToast("Company updated successfully", "success")
				await this.fetchCompanies()

			}

			catch (error) {

				showToast(error.response?.data?.message || "Failed to update company", "danger")

			}
			finally {
				this.updatingId = null
			}

		}

	}

}

</script>

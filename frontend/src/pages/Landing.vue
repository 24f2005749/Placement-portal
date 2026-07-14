<template>
    <main>
        <nav class="navbar navbar-expand-lg bg-dark border-bottom">
            <div class="container">
                <router-link class="navbar-brand fw-bold text-primary" to="/">
                    Placement Portal
                </router-link>

                <div class="d-flex gap-2">
                    <router-link class="btn btn-outline-primary" to="/login">
                        Login
                    </router-link>
                    <router-link class="btn btn-outline-primary" to="/register">
                        Register
                    </router-link>
                </div>
            </div>
        </nav>

        <section class="bg-dark border-bottom">
            <div class="container py-5">
                <div class="row align-items-center g-4 py-lg-5">
                    <div class="col-lg-7">
                        <p class="text-uppercase text-primary fw-semibold small mb-2">
                            University placement management
                        </p>
                        <h1 class="display-5 fw-bold mb-3">
                            Placement Portal
                        </h1>
                        <p class="lead text-secondary mb-4">
                            A focused workspace for students, companies, and administrators to manage placement drives, applications, and approvals.
                        </p>
                        <div class="d-flex flex-wrap gap-2">
                            <router-link class="btn btn-outline-primary btn-lg" to="/register">
                                Get Started
                            </router-link>
                            <router-link class="btn btn-outline-secondary btn-lg" to="/login">
                                Sign In
                            </router-link>
                        </div>
                    </div>

                    <div class="col-lg-5">
                        <div class="bg-dark border rounded-3 shadow-sm p-4">
                            <div class="d-flex justify-content-between border-bottom pb-3 mb-3">
                                <span class="fw-semibold">Student</span>
                                <span class="badge text-bg-success">Apply</span>
                            </div>
                            <div class="d-flex justify-content-between border-bottom pb-3 mb-3">
                                <span class="fw-semibold">Company</span>
                                <span class="badge text-bg-warning">Await approval</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="fw-semibold">Admin</span>
                                <span class="badge text-bg-primary">Review</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
</template>

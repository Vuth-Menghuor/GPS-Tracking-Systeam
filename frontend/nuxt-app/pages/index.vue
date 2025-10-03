<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-blue-600 text-white shadow-lg">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-bold flex items-center">
          <Icon name="mdi:map-marker-radius" class="mr-3 text-4xl" />
          GPS Tracking System Dashboard
        </h1>
        <p class="text-blue-200 mt-2">
          Manage and monitor your GPS tracking devices
        </p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
              <Icon name="mdi:devices" class="text-2xl" />
            </div>
            <div>
              <p class="text-sm text-gray-600">Total Devices</p>
              <p class="text-2xl font-bold text-gray-900">
                {{ stats.total_devices }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-green-100 text-green-600 mr-4">
              <Icon name="mdi:map-marker-check" class="text-2xl" />
            </div>
            <div>
              <p class="text-sm text-gray-600">With GPS</p>
              <p class="text-2xl font-bold text-gray-900">
                {{ stats.with_coordinates }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-red-100 text-red-600 mr-4">
              <Icon name="mdi:map-marker-off" class="text-2xl" />
            </div>
            <div>
              <p class="text-sm text-gray-600">No GPS</p>
              <p class="text-2xl font-bold text-gray-900">
                {{ stats.without_coordinates }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-purple-100 text-purple-600 mr-4">
              <Icon name="mdi:clock-outline" class="text-2xl" />
            </div>
            <div>
              <p class="text-sm text-gray-600">Last Updated</p>
              <p class="text-sm font-semibold text-gray-900">
                {{ lastUpdated }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Icon name="mdi:cog" class="mr-2" />
          Actions
        </h2>

        <div class="flex flex-wrap gap-4">
          <button
            class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-3 rounded-lg flex items-center font-semibold transition duration-200"
            :disabled="loading.fetch"
            @click="fetchTrackingData"
          >
            <Icon name="mdi:download" class="mr-2" />
            {{ loading.fetch ? "Fetching..." : "Fetch GPS Data" }}
          </button>

          <button
            class="bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white px-6 py-3 rounded-lg flex items-center font-semibold transition duration-200"
            :disabled="loading.export"
            @click="exportToCsv"
          >
            <Icon name="mdi:file-export" class="mr-2" />
            {{ loading.export ? "Exporting..." : "Export to CSV" }}
          </button>

          <button
            class="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white px-6 py-3 rounded-lg flex items-center font-semibold transition duration-200"
            :disabled="loading.refresh"
            @click="refreshData"
          >
            <Icon name="mdi:refresh" class="mr-2" />
            {{ loading.refresh ? "Refreshing..." : "Refresh Data" }}
          </button>

          <button
            :class="
              isAutoRefresh
                ? 'bg-green-600 hover:bg-green-700'
                : 'bg-gray-600 hover:bg-gray-700'
            "
            class="text-white px-6 py-3 rounded-lg flex items-center font-semibold transition duration-200"
            @click="toggleAutoRefresh"
          >
            <Icon
              :name="isAutoRefresh ? 'mdi:pause' : 'mdi:play'"
              class="mr-2"
            />
            <div class="flex flex-col items-start">
              <span>{{
                isAutoRefresh ? "Auto-Refresh ON" : "Auto-Refresh OFF"
              }}</span>
              <span v-if="isAutoRefresh" class="text-xs opacity-80">
                GPS fetch in: {{ GPS_FETCH_INTERVAL - autoRefreshCounter }}
              </span>
            </div>
          </button>
        </div>

        <!-- Load to Database Section -->
        <div
          v-if="latestLogFile"
          class="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg"
        >
          <h3 class="font-semibold text-yellow-800 mb-2">
            Latest GPS Data Available
          </h3>
          <p class="text-sm text-yellow-700 mb-3">{{ latestLogFile.folder }}</p>
          <div class="flex gap-3">
            <button
              class="bg-yellow-600 hover:bg-yellow-700 disabled:bg-yellow-400 text-white px-4 py-2 rounded flex items-center text-sm font-semibold transition duration-200"
              :disabled="loading.load"
              @click="loadToDatabase(false)"
            >
              <Icon name="mdi:database-plus" class="mr-1" />
              {{ loading.load ? "Loading..." : "Load to Database" }}
            </button>
            <button
              class="bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white px-4 py-2 rounded flex items-center text-sm font-semibold transition duration-200"
              :disabled="loading.load"
              @click="loadToDatabase(true)"
            >
              <Icon name="mdi:database-refresh" class="mr-1" />
              {{ loading.load ? "Loading..." : "Replace All Data" }}
            </button>
          </div>
        </div>
      </div>

      <!-- Device Data Table -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-900 flex items-center">
            <Icon name="mdi:table" class="mr-2" />
            Device Records
          </h2>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Rank
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  IMEI
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Coordinates
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Last Update
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Time Since Update
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Data Status
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="(device, index) in devices"
                :key="device.ranking_id"
                class="hover:bg-gray-50"
              >
                <td
                  class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                >
                  #{{
                    (pagination.current_page - 1) * pagination.per_page +
                    index +
                    1
                  }}
                </td>
                <td
                  class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 font-mono"
                >
                  {{ device.imei }}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  <span
                    v-if="
                      device.latitude &&
                      device.longitude &&
                      device.latitude !== 0 &&
                      device.longitude !== 0
                    "
                  >
                    {{ device.latitude.toFixed(6) }},
                    {{ device.longitude.toFixed(6) }}
                  </span>
                  <span v-else class="text-gray-400">No GPS data</span>
                </td>
                <td class="px-4 py-4 whitespace-nowrap">
                  <span
                    :class="getStatusColor(device.status)"
                    class="px-2 py-1 text-xs font-semibold rounded-full"
                  >
                    {{ device.status }}
                  </span>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div v-if="device.hearttime_date">
                    <div>{{ device.hearttime_date }}</div>
                    <div class="text-xs text-gray-500">
                      {{ device.hearttime_time }}
                    </div>
                  </div>
                  <span v-else class="text-gray-400">No data</span>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div
                    v-if="
                      device.last_update_relative &&
                      device.last_update_relative !== 'Never'
                    "
                  >
                    <div
                      class="font-medium"
                      :class="getRelativeTimeColor(device.last_update_relative)"
                    >
                      {{ device.last_update_relative }}
                    </div>
                    <div class="text-xs text-gray-500 font-mono">
                      {{ device.last_update_detailed }}
                    </div>
                  </div>
                  <span v-else class="text-gray-400">Never updated</span>
                </td>
                <td class="px-4 py-4 whitespace-nowrap">
                  <span
                    :class="getDataStatusColor(device.datastatus_description)"
                    class="px-2 py-1 text-xs font-semibold rounded-full"
                  >
                    {{ device.datastatus_description }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div
          class="bg-gray-50 px-6 py-3 flex items-center justify-between border-t border-gray-200"
        >
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="!pagination.has_previous"
              @click="previousPage"
            >
              Previous
            </button>
            <button
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="!pagination.has_next"
              @click="nextPage"
            >
              Next
            </button>
          </div>
          <div
            class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"
          >
            <div>
              <p class="text-sm text-gray-700">
                Showing page
                <span class="font-medium">{{ pagination.current_page }}</span>
                of
                <span class="font-medium">{{ pagination.total_pages }}</span>
                ({{ pagination.total_records }} total records)
              </p>
            </div>
            <div class="flex space-x-2">
              <button
                class="relative inline-flex items-center px-3 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed rounded-md"
                :disabled="!pagination.has_previous"
                @click="previousPage"
              >
                <Icon name="mdi:chevron-left" />
              </button>
              <button
                class="relative inline-flex items-center px-3 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed rounded-md"
                :disabled="!pagination.has_next"
                @click="nextPage"
              >
                <Icon name="mdi:chevron-right" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Toast Notifications -->
    <div v-if="message.text" class="fixed top-4 right-4 z-50">
      <div
        :class="{
          'bg-green-500': message.type === 'success',
          'bg-red-500': message.type === 'error',
          'bg-blue-500': message.type === 'info',
        }"
        class="text-white px-6 py-4 rounded-lg shadow-lg flex items-center"
      >
        <Icon
          :name="
            message.type === 'success'
              ? 'mdi:check-circle'
              : message.type === 'info'
              ? 'mdi:information'
              : 'mdi:alert-circle'
          "
          class="mr-2"
        />
        {{ message.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
// Meta and head
useHead({
  title: "GPS Tracking Dashboard",
  meta: [
    {
      name: "description",
      content: "GPS Tracking System Dashboard for monitoring devices",
    },
  ],
});

// Reactive data
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const stats = ref({
  total_devices: 0,
  with_coordinates: 0,
  without_coordinates: 0,
  status_counts: {},
});

const devices = ref([]);
const pagination = ref({
  current_page: 1,
  total_pages: 1,
  total_records: 0,
  per_page: 50,
  has_next: false,
  has_previous: false,
});

const loading = ref({
  fetch: false,
  export: false,
  refresh: false,
  load: false,
});

const message = ref({
  text: "",
  type: "success",
});

const latestLogFile = ref(null);
const lastUpdated = ref("");

// Methods
const showMessage = (text, type = "success") => {
  message.value = { text, type };
  setTimeout(
    () => {
      message.value = { text: "", type: "success" };
    },
    type === "info" ? 3000 : 5000
  ); // Shorter duration for info messages
};

const getStatusColor = (status) => {
  if (status === "success") return "bg-green-100 text-green-800";
  if (status.includes("error") || status.includes("can't access"))
    return "bg-red-100 text-red-800";
  return "bg-yellow-100 text-yellow-800";
};

const getDataStatusColor = (status) => {
  if (status === "Online") return "bg-green-100 text-green-800";
  if (status === "Offline") return "bg-red-100 text-red-800";
  if (status === "Expired") return "bg-orange-100 text-orange-800";
  return "bg-gray-100 text-gray-800";
};

const getRelativeTimeColor = (relativeTime) => {
  if (!relativeTime || relativeTime === "Never") return "text-gray-400";

  // Recent updates (green)
  if (
    relativeTime.includes("min ago") ||
    relativeTime.includes("hour") ||
    relativeTime === "Just now"
  ) {
    return "text-green-600 font-semibold";
  }

  // Today or yesterday (green)
  if (relativeTime === "Today" || relativeTime === "1 day ago") {
    return "text-green-600";
  }

  // Within a week (yellow/orange)
  if (
    relativeTime.includes("day") &&
    !relativeTime.includes("year") &&
    !relativeTime.includes("month")
  ) {
    const days = parseInt(relativeTime.match(/\d+/)?.[0] || "0");
    if (days <= 7) return "text-yellow-600";
  }

  // Within a month (orange)
  if (
    relativeTime.includes("week") ||
    (relativeTime.includes("day") &&
      parseInt(relativeTime.match(/\d+/)?.[0] || "0") <= 30)
  ) {
    return "text-orange-600";
  }

  // Older than a month (red)
  if (relativeTime.includes("month") || relativeTime.includes("year")) {
    return "text-red-600 font-semibold";
  }

  return "text-gray-600";
};

const fetchStats = async () => {
  try {
    const response = await $fetch(`${apiBase}/stats/`);
    if (response.success) {
      stats.value = response.stats;
    }
  } catch (error) {
    console.error("Error fetching stats:", error);
  }
};

const fetchDevices = async (page = 1) => {
  try {
    const response = await $fetch(
      `${apiBase}/devices/?page=${page}&per_page=50`
    );
    if (response.success) {
      devices.value = response.data;
      pagination.value = response.pagination;
      lastUpdated.value = new Date().toLocaleString();
    }
  } catch (error) {
    console.error("Error fetching devices:", error);
    showMessage("Error loading device data", "error");
  }
};

const fetchRecentLogs = async () => {
  try {
    const response = await $fetch(`${apiBase}/logs/`);
    if (response.success && response.logs.length > 0) {
      latestLogFile.value = response.logs[0];
    }
  } catch (error) {
    console.error("Error fetching logs:", error);
  }
};

const fetchTrackingData = async () => {
  loading.value.fetch = true;
  try {
    const response = await $fetch(`${apiBase}/fetch-tracking/`, {
      method: "POST",
    });
    if (response.success) {
      showMessage("GPS tracking data fetched successfully!");
      if (response.json_file) {
        latestLogFile.value = {
          folder: response.folder,
          json_file: response.json_file,
        };
      }
      await fetchRecentLogs();
    } else {
      showMessage(response.error || "Error fetching tracking data", "error");
    }
  } catch (error) {
    console.error("Error:", error);
    showMessage("Error fetching tracking data", "error");
  }
  loading.value.fetch = false;
};

const loadToDatabase = async (clearExisting = false) => {
  if (!latestLogFile.value) {
    showMessage("No GPS data file available to load", "error");
    return;
  }

  loading.value.load = true;
  try {
    const response = await $fetch(`${apiBase}/load-database/`, {
      method: "POST",
      body: {
        json_file: latestLogFile.value.json_file,
        clear_existing: clearExisting,
      },
    });
    if (response.success) {
      showMessage(response.message);
      await Promise.all([fetchStats(), fetchDevices()]);
    } else {
      showMessage(response.error || "Error loading data to database", "error");
    }
  } catch (error) {
    console.error("Error:", error);
    showMessage("Error loading data to database", "error");
  }
  loading.value.load = false;
};

const exportToCsv = async () => {
  loading.value.export = true;
  try {
    // Create a link and trigger download
    const response = await fetch(`${apiBase}/export-csv/`);
    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;

      // Get filename from Content-Disposition header or use default
      const contentDisposition = response.headers.get("Content-Disposition");
      const filename = contentDisposition
        ? contentDisposition.split("filename=")[1].replace(/"/g, "")
        : `gps_tracking_data_${new Date()
            .toISOString()
            .slice(0, 19)
            .replace(/:/g, "-")}.csv`;

      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      showMessage("CSV file exported successfully!");
    } else {
      showMessage("Error exporting CSV file", "error");
    }
  } catch (error) {
    console.error("Error:", error);
    showMessage("Error exporting CSV file", "error");
  }
  loading.value.export = false;
};

const refreshData = async () => {
  loading.value.refresh = true;
  await Promise.all([
    fetchStats(),
    fetchDevices(pagination.value.current_page),
    fetchRecentLogs(),
  ]);
  showMessage("Data refreshed successfully!");
  loading.value.refresh = false;
};

const nextPage = () => {
  if (pagination.value.has_next) {
    fetchDevices(pagination.value.current_page + 1);
  }
};

const previousPage = () => {
  if (pagination.value.has_previous) {
    fetchDevices(pagination.value.current_page - 1);
  }
};

// Auto-refresh functionality
const autoRefreshInterval = ref(null);
const isAutoRefresh = ref(true);
const autoRefreshCounter = ref(0);
const REFRESH_INTERVAL = 30000; // 30 seconds for UI updates
const GPS_FETCH_INTERVAL = 5; // Fetch new GPS data every 5 UI refreshes (2.5 minutes)

const startAutoRefresh = () => {
  if (autoRefreshInterval.value) {
    clearInterval(autoRefreshInterval.value);
  }

  if (isAutoRefresh.value) {
    // Refresh every 30 seconds to update relative times
    autoRefreshInterval.value = setInterval(async () => {
      // Always update the display (for time since update)
      await fetchDevices(pagination.value.current_page);

      // Increment counter and fetch new GPS data periodically
      autoRefreshCounter.value++;

      // Every 5 refreshes (2.5 minutes), fetch new GPS data from API
      if (autoRefreshCounter.value >= GPS_FETCH_INTERVAL) {
        autoRefreshCounter.value = 0;

        // Show a subtle indicator that we're fetching new GPS data
        showMessage("Auto-fetching fresh GPS data...", "info");

        try {
          // Fetch new tracking data from API
          const response = await $fetch(`${apiBase}/fetch-tracking/`, {
            method: "POST",
          });

          if (response.success) {
            // Auto-load the new data to database if successful
            if (response.json_file) {
              await $fetch(`${apiBase}/load-database/`, {
                method: "POST",
                body: {
                  json_file: response.json_file,
                  clear_existing: false, // Don't clear, just update
                },
              });

              // Refresh all data after loading new GPS coordinates
              await Promise.all([
                fetchStats(),
                fetchDevices(pagination.value.current_page),
                fetchRecentLogs(),
              ]);

              showMessage("GPS coordinates updated automatically!", "success");
            }
          }
        } catch (error) {
          console.error("Auto GPS fetch error:", error);
          // Don't show error message to avoid spam, just log it
        }
      }
    }, REFRESH_INTERVAL);
  }
};

const toggleAutoRefresh = () => {
  isAutoRefresh.value = !isAutoRefresh.value;
  if (isAutoRefresh.value) {
    autoRefreshCounter.value = 0; // Reset counter
    startAutoRefresh();
    showMessage(
      "Auto-refresh enabled (30s intervals + GPS updates every 2.5min)"
    );
  } else {
    if (autoRefreshInterval.value) {
      clearInterval(autoRefreshInterval.value);
      autoRefreshInterval.value = null;
    }
    showMessage("Auto-refresh disabled");
  }
};

// Initialize data on mount
onMounted(async () => {
  await Promise.all([fetchStats(), fetchDevices(), fetchRecentLogs()]);
  startAutoRefresh();
});

// Cleanup on unmount
onUnmounted(() => {
  if (autoRefreshInterval.value) {
    clearInterval(autoRefreshInterval.value);
  }
});
</script>

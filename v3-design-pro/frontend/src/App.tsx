import React, { useState, useEffect, useRef } from "react";
import L from "leaflet";
import {
  Radio,
  Search,
  Map as MapIcon,
  Package,
  BarChart3,
  Lock,
  Unlock,
  LogOut,
  Trash2,
  Plus,
  RefreshCw,
  Bell,
  BellOff,
  FileText,
  Clock,
  User,
  Upload,
  Download,
  AlertTriangle,
  CheckCircle2,
  MapPin,
  Activity,
  Info,
  X,
  FileCheck
} from "lucide-react";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Button } from "./components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./components/ui/card";
import { MagicCard } from "./components/magicui/magic-card";
import { PulsatingButton } from "./components/magicui/pulsating-button";

// Fix Leaflet marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

interface UserSession {
  username: string;
  role: string;
}

export default function App() {
  // Authentication state
  const [user, setUser] = useState<UserSession | null>(() => {
    const saved = localStorage.getItem("dolphisic_user");
    return saved ? JSON.parse(saved) : null;
  });
  const [usernameInput, setUsernameInput] = useState("");
  const [passwordInput, setPasswordInput] = useState("");
  const [authError, setAuthError] = useState("");
  const [loading, setLoading] = useState(false);

  // Tab State
  const [activeTab, setActiveTab] = useState<"inventory" | "search" | "carto" | "stock" | "stats">("inventory");

  // Global centers
  const [cisList, setCisList] = useState<string[]>([]);
  const [selectedCis, setSelectedCis] = useState<string>("");

  // Global settings modal
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [notifSettings, setNotifSettings] = useState({
    global_notification_enabled: false,
    notify_exceeded: true,
    notify_approaching: true,
    email_notif: "",
  });

  // --- 1. INVENTORY TAB STATE ---
  const [selectedType, setSelectedType] = useState<string>("BIP");
  const [devices, setDevices] = useState<any[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<any | null>(null);
  const [showAddDeviceModal, setShowAddDeviceModal] = useState(false);
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [newDevice, setNewDevice] = useState({
    modele: "",
    num_serie: "",
    affectation: "",
    version_logiciel: "",
    observation: "",
    date_maj_cle: "",
  });
  const [updatingCryptageId, setUpdatingCryptageId] = useState<number | null>(null);
  const [newCryptageDate, setNewCryptageDate] = useState("");

  // --- 2. ADVANCED SEARCH STATE ---
  const [searchForm, setSearchForm] = useState({
    cis: "",
    modele: "",
    type: "",
    num_serie: "",
    affectation: "",
    observation: "",
    version_logiciel: "",
  });
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searchMetadata, setSearchMetadata] = useState<{ centres: string[]; modeles: string[]; types: string[] }>({
    centres: [],
    modeles: [],
    types: [],
  });

  // --- 3. STATISTICS TAB STATE ---
  const [statsData, setStatsData] = useState<any>({
    by_model: [],
    by_type: [],
    by_centre: [],
    total_equipments: 0,
  });

  // --- 4. STOCK & LOANS TAB STATE ---
  const [stockItems, setStockItems] = useState<any[]>([]);
  const [selectedStockItem, setSelectedStockItem] = useState<any | null>(null);
  const [showAddStockModal, setShowAddStockModal] = useState(false);
  const [stockHistory, setStockHistory] = useState<any[]>([]);
  const [newStockItem, setNewStockItem] = useState({
    nom: "",
    description: "",
    type_materiel: "BIP",
    etat: "Neuf",
    modele: "",
    num_serie: "",
    cis: "",
    pocsag: "",
    rfgi: "",
    identifiant: "",
  });
  const [showLoanModal, setShowLoanModal] = useState<any | null>(null);
  const [loanForm, setLoanForm] = useState({
    emprunteur: "",
    date_debut: new Date().toISOString().split("T")[0],
    date_fin: "",
  });
  const [showReturnModal, setShowReturnModal] = useState<any | null>(null);
  const [returnForm, setReturnForm] = useState({
    changement_etat: "",
    nouveau_statut_etat: "",
  });

  // --- 5. CARTOGRAPHY TAB STATE & REFS ---
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const leafletMap = useRef<L.Map | null>(null);
  const sitesLayer = useRef<L.LayerGroup | null>(null);
  const liaisonsLayer = useRef<L.LayerGroup | null>(null);
  const labelsLayer = useRef<L.LayerGroup | null>(null);

  const [cartoData, setCartoData] = useState<{ sites: any[]; labels: any[]; liaisons: any[] }>({
    sites: [],
    labels: [],
    liaisons: [],
  });
  const [mapMode, setMapMode] = useState<"view" | "add_site" | "add_label" | "add_liaison">("view");
  const [selectedSite, setSelectedSite] = useState<any | null>(null);
  const [selectedLiaison, setSelectedLiaison] = useState<any | null>(null);
  const [activeSiteTab, setActiveSiteTab] = useState<"inventaire" | "taches" | "pylones" | "log" | "documents">("inventaire");

  // Site dialog / modal when adding new site or label
  const [clickCoords, setClickCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [newSiteForm, setNewSiteForm] = useState({ nom: "", type: "Point Haut" });
  const [newLabelForm, setNewLabelForm] = useState({ texte: "" });

  // Add liaison source state
  const [showLiaisonModal, setShowLiaisonModal] = useState<{ siteA: any; siteB: any } | null>(null);
  const [newLiaisonForm, setNewLiaisonForm] = useState({ label: "", couleur: "#00FF00" });

  // Site detail tabs data
  const [siteInfo, setSiteInfo] = useState({ inventaire: "", taches: "" });
  const [pylones, setPylones] = useState<any[]>([]);
  const [newPyloneName, setNewPyloneName] = useState("");
  const [newPyloneDesc, setNewPyloneDesc] = useState("");
  const [mainCourante, setMainCourante] = useState<any[]>([]);
  const [newEventText, setNewEventText] = useState("");
  const [documents, setDocuments] = useState<any[]>([]);
  const [uploadFile, setUploadFile] = useState<File | null>(null);

  // ----------------------------------------------------
  // INITIAL DATA FETCH & TELEMETRY LOGGER
  // ----------------------------------------------------
  useEffect(() => {
    if (user) {
      fetchCis();
      fetchSearchMetadata();
      fetchNotificationSettings();
    }
  }, [user]);

  // Fetch CIS List
  const fetchCis = async () => {
    try {
      const res = await fetch("/api/centres");
      const data = await res.json();
      if (Array.isArray(data)) {
        setCisList(data);
        if (data.length > 0 && !selectedCis) {
          setSelectedCis(data[0]);
        }
      }
    } catch (e) {
      console.error("Error fetching centres", e);
    }
  };

  // Fetch notification settings
  const fetchNotificationSettings = async () => {
    try {
      const res = await fetch("/api/notifications/settings");
      const data = await res.json();
      if (data && !data.error) {
        setNotifSettings(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Save notification settings
  const saveNotificationSettings = async () => {
    try {
      const res = await fetch("/api/notifications/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(notifSettings),
      });
      const data = await res.json();
      if (data.success) {
        setShowSettingsModal(false);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Log UI interactions manually if needed
  const logUIInteraction = (event: string, label: string, details: any = {}) => {
    fetch("/api/logs/ui", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        event,
        path: activeTab,
        details: { label, ...details },
      }),
    }).catch(() => {});
  };

  // ----------------------------------------------------
  // LOGIN / LOGOUT
  // ----------------------------------------------------
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError("");
    setLoading(true);
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: usernameInput, password: passwordInput }),
      });
      const data = await res.json();
      if (data.success) {
        setUser(data.user);
        localStorage.setItem("dolphisic_user", JSON.stringify(data.user));
      } else {
        setAuthError(data.error || "Identifiants invalides");
      }
    } catch (err) {
      setAuthError("Erreur serveur lors de la connexion");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("dolphisic_user");
    logUIInteraction("LOGOUT", "Déconnexion");
  };

  // ----------------------------------------------------
  // 1. INVENTORY TAB ACTIONS
  // ----------------------------------------------------
  const fetchDevices = async () => {
    if (!selectedCis || !selectedType) return;
    try {
      const res = await fetch(`/api/devices?cis=${encodeURIComponent(selectedCis)}&type=${selectedType}`);
      const data = await res.json();
      if (Array.isArray(data)) {
        setDevices(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (user && activeTab === "inventory") {
      fetchDevices();
    }
  }, [selectedCis, selectedType, activeTab]);

  // Fetch models for adding device
  useEffect(() => {
    if (showAddDeviceModal && selectedType) {
      fetch(`/api/modeles?type=${selectedType}`)
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data)) {
            setAvailableModels(data);
            if (data.length > 0) {
              setNewDevice((prev) => ({ ...prev, modele: data[0] }));
            }
          }
        });
    }
  }, [showAddDeviceModal, selectedType]);

  const handleAddDevice = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/devices", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cis: selectedCis,
          modele: newDevice.modele,
          num_serie: newDevice.num_serie,
          affectation: newDevice.affectation,
          version_logiciel: newDevice.version_logiciel,
          observation: newDevice.observation,
          date_maj_cle: newDevice.date_maj_cle || null,
        }),
      });
      const data = await res.json();
      if (data.success) {
        setShowAddDeviceModal(false);
        setNewDevice({
          modele: "",
          num_serie: "",
          affectation: "",
          version_logiciel: "",
          observation: "",
          date_maj_cle: "",
        });
        fetchDevices();
        logUIInteraction("SUBMIT", "Ajout équipement parc", { modele: newDevice.modele });
      } else {
        alert(data.error || "Erreur lors de l'ajout");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpdateCryptage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!updatingCryptageId || !newCryptageDate) return;
    try {
      const res = await fetch(`/api/devices/${updatingCryptageId}/update-cryptage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date_maj_cle: newCryptageDate }),
      });
      const data = await res.json();
      if (data.success) {
        setUpdatingCryptageId(null);
        setNewCryptageDate("");
        fetchDevices();
        if (selectedDevice && selectedDevice.id === updatingCryptageId) {
          fetchDeviceDetails(updatingCryptageId);
        }
        logUIInteraction("SUBMIT", "Mise à jour chiffrement", { id: updatingCryptageId });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleAlert = async (device: any) => {
    const nextState = !device.notification_active;
    const email = nextState ? notifSettings.email_notif || prompt("Saisir l'email d'alerte :") : null;
    if (nextState && !email) return;

    try {
      const res = await fetch(`/api/devices/${device.id}/toggle-notification`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ notification_active: nextState, email_notif: email }),
      });
      const data = await res.json();
      if (data.success) {
        fetchDevices();
        if (selectedDevice && selectedDevice.id === device.id) {
          fetchDeviceDetails(device.id);
        }
        logUIInteraction("CHANGE", "Alerte de chiffrement", { id: device.id, value: nextState });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteDevice = async (id: number) => {
    if (!confirm("Voulez-vous vraiment supprimer cet équipement du parc ?")) return;
    try {
      const res = await fetch(`/api/devices/${id}/delete`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        setSelectedDevice(null);
        fetchDevices();
        logUIInteraction("CLICK", "Suppression équipement parc", { id });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchDeviceDetails = async (id: number) => {
    try {
      const res = await fetch(`/api/devices/${id}`);
      const data = await res.json();
      if (data && !data.error) {
        setSelectedDevice(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // ----------------------------------------------------
  // 2. ADVANCED SEARCH ACTIONS
  // ----------------------------------------------------
  const fetchSearchMetadata = async () => {
    try {
      const res = await fetch("/api/search/metadata");
      const data = await res.json();
      if (data && !data.error) {
        setSearchMetadata(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleAdvancedSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(searchForm),
      });
      const data = await res.json();
      if (Array.isArray(data)) {
        setSearchResults(data);
        logUIInteraction("SUBMIT", "Recherche avancée", searchForm);
      }
    } catch (err) {
      console.error(err);
    }
  };

  // ----------------------------------------------------
  // 3. STATS ACTIONS
  // ----------------------------------------------------
  const fetchStats = async () => {
    try {
      const res = await fetch("/api/stats");
      const data = await res.json();
      if (data && !data.error) {
        setStatsData(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (user && activeTab === "stats") {
      fetchStats();
    }
  }, [activeTab]);

  // ----------------------------------------------------
  // 4. STOCK & LOANS ACTIONS
  // ----------------------------------------------------
  const fetchStock = async () => {
    try {
      const res = await fetch("/api/stock");
      const data = await res.json();
      if (Array.isArray(data)) {
        setStockItems(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (user && activeTab === "stock") {
      fetchStock();
    }
  }, [activeTab]);

  const handleAddStock = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/stock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newStockItem),
      });
      const data = await res.json();
      if (data.success) {
        setShowAddStockModal(false);
        setNewStockItem({
          nom: "",
          description: "",
          type_materiel: "BIP",
          etat: "Neuf",
          modele: "",
          num_serie: "",
          cis: "",
          pocsag: "",
          rfgi: "",
          identifiant: "",
        });
        fetchStock();
        logUIInteraction("SUBMIT", "Ajout matériel stock", { nom: newStockItem.nom });
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteStock = async (id: number) => {
    if (!confirm("Voulez-vous vraiment retirer ce matériel du stock ?")) return;
    try {
      const res = await fetch(`/api/stock/${id}`, { method: "DELETE" });
      const data = await res.json();
      if (data.success) {
        setSelectedStockItem(null);
        fetchStock();
        logUIInteraction("CLICK", "Retrait matériel stock", { id });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreateLoan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!showLoanModal) return;
    try {
      const res = await fetch(`/api/stock/${showLoanModal.id}/prets`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loanForm),
      });
      const data = await res.json();
      if (data.success) {
        setShowLoanModal(null);
        setLoanForm({
          emprunteur: "",
          date_debut: new Date().toISOString().split("T")[0],
          date_fin: "",
        });
        fetchStock();
        logUIInteraction("SUBMIT", "Enregistrement prêt matériel", { item_id: showLoanModal.id });
      } else {
        alert(data.error);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleReturnLoan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!showReturnModal) return;
    try {
      const res = await fetch(`/api/prets/${showReturnModal.active_pret_id}/retour`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(returnForm),
      });
      const data = await res.json();
      if (data.success) {
        setShowReturnModal(null);
        setReturnForm({ changement_etat: "", nouveau_statut_etat: "" });
        fetchStock();
        logUIInteraction("SUBMIT", "Retour matériel prêté", { pret_id: showReturnModal.active_pret_id });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchLoanHistory = async (itemId: number) => {
    try {
      const res = await fetch(`/api/stock/${itemId}/prets`);
      const data = await res.json();
      if (Array.isArray(data)) {
        setStockHistory(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  // ----------------------------------------------------
  // 5. CARTOGRAPHY & MAP ACTIONS
  // ----------------------------------------------------
  const fetchCartoData = async () => {
    try {
      const res = await fetch("/api/carto");
      const data = await res.json();
      if (data && !data.error) {
        setCartoData(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Fetch map elements on carto tab enter
  useEffect(() => {
    if (user && activeTab === "carto") {
      fetchCartoData();
    }
  }, [activeTab]);

  // Leaflet map renderer effect
  useEffect(() => {
    if (activeTab !== "carto" || !mapContainerRef.current) return;

    if (!leafletMap.current) {
      const map = L.map(mapContainerRef.current).setView([44.1, 6.2], 9);
      leafletMap.current = map;

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: "© OpenStreetMap contributors",
      }).addTo(map);

      sitesLayer.current = L.layerGroup().addTo(map);
      liaisonsLayer.current = L.layerGroup().addTo(map);
      labelsLayer.current = L.layerGroup().addTo(map);

      // Map click handler for adding elements
      map.on("click", (e: L.LeafletMouseEvent) => {
        // Ref to mapMode via raw JS because inside closure
        const currentMode = (document.getElementById("map-mode-selector") as HTMLSelectElement)?.value || "view";
        if (currentMode === "add_site") {
          setClickCoords({ lat: e.latlng.lat, lng: e.latlng.lng });
          setNewSiteForm({ nom: "", type: "Point Haut" });
        } else if (currentMode === "add_label") {
          setClickCoords({ lat: e.latlng.lat, lng: e.latlng.lng });
          setNewLabelForm({ texte: "" });
        }
      });
    }

    return () => {
      // Map cleanup on unmount or navigation
      if (leafletMap.current) {
        leafletMap.current.remove();
        leafletMap.current = null;
        sitesLayer.current = null;
        liaisonsLayer.current = null;
        labelsLayer.current = null;
      }
    };
  }, [activeTab]);

  // Re-draw map markers whenever cartoData changes
  useEffect(() => {
    if (activeTab !== "carto" || !leafletMap.current || !sitesLayer.current || !liaisonsLayer.current || !labelsLayer.current) return;

    // Clear old layers
    sitesLayer.current.clearLayers();
    liaisonsLayer.current.clearLayers();
    labelsLayer.current.clearLayers();

    // Render sites
    cartoData.sites.forEach((site) => {
      const isPointHaut = site.type === "Point Haut";
      const isCis = site.type === "CIS";
      const color = isPointHaut ? "#ef4444" : isCis ? "#3b82f6" : site.type === "Centre Mixte" ? "#10b981" : "#f59e0b";
      const fillColor = isPointHaut ? "#991b1b" : isCis ? "#1e3a8a" : site.type === "Centre Mixte" ? "#065f46" : "#92400e";

      const marker = L.circleMarker([site.latitude, site.longitude], {
        radius: 9,
        color: color,
        fillColor: fillColor,
        fillOpacity: 0.85,
        weight: 2,
      });

      marker.bindTooltip(site.nom, { permanent: false, direction: "top" });

      marker.on("click", () => {
        // Handle liaison drawing
        const currentMode = (document.getElementById("map-mode-selector") as HTMLSelectElement)?.value || "view";
        if (currentMode === "add_liaison") {
          const firstSite = JSON.parse((document.getElementById("liaison-first-site") as HTMLInputElement)?.value || "null");
          if (!firstSite) {
            // Pick first site
            (document.getElementById("liaison-first-site") as HTMLInputElement)!.value = JSON.stringify(site);
            alert(`Site source sélectionné : ${site.nom}. Cliquez sur le site destinataire.`);
          } else {
            // Pick second site & open popup
            if (firstSite.id === site.id) {
              alert("Le site destinataire doit être différent.");
              return;
            }
            setShowLiaisonModal({ siteA: firstSite, siteB: site });
            setNewLiaisonForm({ label: "", couleur: "#00FF00" });
            (document.getElementById("liaison-first-site") as HTMLInputElement)!.value = ""; // reset
          }
        } else {
          // Normal selection
          setSelectedSite(site);
          setSelectedLiaison(null);
        }
      });

      marker.addTo(sitesLayer.current!);
    });

    // Render liaisons
    cartoData.liaisons.forEach((liaison) => {
      const line = L.polyline(
        [
          [liaison.lat_a, liaison.lng_a],
          [liaison.lat_b, liaison.lng_b],
        ],
        {
          color: liaison.couleur || "#00FF00",
          weight: 4,
          opacity: 0.85,
        }
      );

      if (liaison.label) {
        line.bindTooltip(liaison.label, { sticky: true });
      }

      line.on("click", () => {
        setSelectedLiaison(liaison);
        setSelectedSite(null);
      });

      line.addTo(liaisonsLayer.current!);
    });

    // Render free labels
    cartoData.labels.forEach((label) => {
      const labelIcon = L.divIcon({
        className: "bg-slate-900/90 border border-slate-800 text-[10px] text-slate-300 font-mono font-semibold px-2 py-0.5 rounded-md shadow shadow-black/80 whitespace-nowrap backdrop-blur-sm",
        html: `
          <div class="flex items-center gap-1.5">
            <span>${label.texte}</span>
            <button onclick="window.deleteLabel(${label.id})" class="text-rose-500 hover:text-rose-400 font-bold ml-1 focus:outline-none">✕</button>
          </div>
        `,
        iconSize: [100, 20] as any,
        iconAnchor: [50, 10] as any,
      });

      const labelMarker = L.marker([label.latitude, label.longitude], { icon: labelIcon });
      labelMarker.addTo(labelsLayer.current!);
    });

    // Expose deleteLabel to window for the raw html button in divIcon
    (window as any).deleteLabel = async (id: number) => {
      if (!confirm("Supprimer ce label libre ?")) return;
      try {
        const res = await fetch(`/api/carto/labels/${id}/delete`, { method: "POST" });
        const data = await res.json();
        if (data.success) {
          fetchCartoData();
        }
      } catch (e) {
        console.error(e);
      }
    };
  }, [cartoData, activeTab]);

  // Load selected site info & tabs data
  useEffect(() => {
    if (selectedSite) {
      // 1. Fetch site text fields (inventaire, taches)
      fetch(`/api/carto/sites/${selectedSite.id}/info`)
        .then((res) => res.json())
        .then((data) => {
          if (data && !data.error) {
            setSiteInfo({ inventaire: data.inventaire || "", taches: data.taches || "" });
          }
        });

      // 2. Fetch Pylones
      fetch(`/api/carto/sites/${selectedSite.id}/pylones`)
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data)) setPylones(data);
        });

      // 3. Fetch Main Courante
      fetch(`/api/carto/sites/${selectedSite.id}/main_courante`)
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data)) setMainCourante(data);
        });

      // 4. Fetch Documents
      fetch(`/api/carto/documents?parent_id=${selectedSite.id}&parent_type=site`)
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data)) setDocuments(data);
        });
    }
  }, [selectedSite]);

  const saveSiteInfo = async () => {
    if (!selectedSite) return;
    try {
      const res = await fetch(`/api/carto/sites/${selectedSite.id}/info`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(siteInfo),
      });
      const data = await res.json();
      if (data.success) {
        alert("Fiche de tâche enregistrée avec succès");
        logUIInteraction("SUBMIT", "Enregistrement fiche site", { id: selectedSite.id });
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddSite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!clickCoords) return;
    try {
      const res = await fetch("/api/carto/sites", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nom: newSiteForm.nom,
          type: newSiteForm.type,
          latitude: clickCoords.lat,
          longitude: clickCoords.lng,
        }),
      });
      const data = await res.json();
      if (data.success) {
        setClickCoords(null);
        fetchCartoData();
        logUIInteraction("SUBMIT", "Ajout site carto", { nom: newSiteForm.nom });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddLabel = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!clickCoords) return;
    try {
      const res = await fetch("/api/carto/labels", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          texte: newLabelForm.texte,
          latitude: clickCoords.lat,
          longitude: clickCoords.lng,
        }),
      });
      const data = await res.json();
      if (data.success) {
        setClickCoords(null);
        fetchCartoData();
        logUIInteraction("SUBMIT", "Ajout label carto", { texte: newLabelForm.texte });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddLiaison = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!showLiaisonModal) return;
    try {
      const res = await fetch("/api/carto/liaisons", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          site_a_id: showLiaisonModal.siteA.id,
          site_b_id: showLiaisonModal.siteB.id,
          label: newLiaisonForm.label,
          couleur: newLiaisonForm.couleur,
        }),
      });
      const data = await res.json();
      if (data.success) {
        setShowLiaisonModal(null);
        fetchCartoData();
        logUIInteraction("SUBMIT", "Ajout liaison carto", { label: newLiaisonForm.label });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteSite = async (siteId: number) => {
    if (!confirm("Voulez-vous vraiment supprimer ce site et toutes ses liaisons/documents/événements associés ?")) return;
    try {
      const res = await fetch(`/api/carto/sites/${siteId}/delete`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        setSelectedSite(null);
        fetchCartoData();
        logUIInteraction("CLICK", "Suppression site carto", { id: siteId });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteLiaison = async (liaisonId: number) => {
    if (!confirm("Supprimer cette liaison radio ?")) return;
    try {
      const res = await fetch(`/api/carto/liaisons/${liaisonId}/delete`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        setSelectedLiaison(null);
        fetchCartoData();
        logUIInteraction("CLICK", "Suppression liaison carto", { id: liaisonId });
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Pylones CRUD
  const handleAddPylone = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSite || !newPyloneName) return;
    try {
      const res = await fetch(`/api/carto/sites/${selectedSite.id}/pylones`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nom_pylone: newPyloneName, description: newPyloneDesc }),
      });
      const data = await res.json();
      if (data.success) {
        setNewPyloneName("");
        setNewPyloneDesc("");
        // Reload pylones
        fetch(`/api/carto/sites/${selectedSite.id}/pylones`)
          .then((r) => r.json())
          .then((d) => setPylones(d));
        logUIInteraction("SUBMIT", "Ajout pylône site", { nom: newPyloneName });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeletePylone = async (id: number) => {
    if (!confirm("Supprimer ce pylône ?")) return;
    try {
      const res = await fetch(`/api/carto/pylones/${id}/delete`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        // Reload pylones
        fetch(`/api/carto/sites/${selectedSite!.id}/pylones`)
          .then((r) => r.json())
          .then((d) => setPylones(d));
        logUIInteraction("CLICK", "Suppression pylône site", { id });
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Main Courante CRUD
  const handleAddEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSite || !newEventText) return;
    try {
      const res = await fetch(`/api/carto/sites/${selectedSite.id}/main_courante`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ evenement: newEventText }),
      });
      const data = await res.json();
      if (data.success) {
        setNewEventText("");
        // Reload history
        fetch(`/api/carto/sites/${selectedSite.id}/main_courante`)
          .then((r) => r.json())
          .then((d) => setMainCourante(d));
        logUIInteraction("SUBMIT", "Ajout événement main courante", { text: newEventText });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteEvent = async (id: number) => {
    if (!confirm("Supprimer cet événement du journal ?")) return;
    try {
      const res = await fetch(`/api/carto/main_courante/${id}/delete`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        // Reload history
        fetch(`/api/carto/sites/${selectedSite!.id}/main_courante`)
          .then((r) => r.json())
          .then((d) => setMainCourante(d));
        logUIInteraction("CLICK", "Suppression événement main courante", { id });
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Documents Upload
  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSite || !uploadFile) return;

    const formData = new FormData();
    formData.append("parent_id", selectedSite.id.toString());
    formData.append("parent_type", "site");
    formData.append("file", uploadFile);

    try {
      const res = await fetch("/api/carto/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.success) {
        setUploadFile(null);
        // Reset file input
        (document.getElementById("file-upload-input") as HTMLInputElement).value = "";
        // Reload documents
        fetch(`/api/carto/documents?parent_id=${selectedSite.id}&parent_type=site`)
          .then((r) => r.json())
          .then((d) => setDocuments(d));
        logUIInteraction("SUBMIT", "Upload document site", { filename: uploadFile.name });
      } else {
        alert(data.error);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteDocument = async (id: number) => {
    if (!confirm("Supprimer ce fichier joint ?")) return;
    try {
      const res = await fetch(`/api/carto/documents/${id}/delete`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        // Reload documents
        fetch(`/api/carto/documents?parent_id=${selectedSite!.id}&parent_type=site`)
          .then((r) => r.json())
          .then((d) => setDocuments(d));
        logUIInteraction("CLICK", "Suppression document site", { id });
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Save Liaison Notes
  const saveLiaisonNotes = async (liaisonId: number, notes: string) => {
    try {
      const res = await fetch(`/api/carto/liaisons/${liaisonId}/info`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ notes }),
      });
      const data = await res.json();
      if (data.success) {
        alert("Notes de liaison sauvegardées");
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Helper: check encryption expiry status
  const getCryptageStatus = (dateStr: string) => {
    if (!dateStr) return { label: "Jamais", color: "text-slate-400 bg-slate-900 border-slate-800" };
    const date = new Date(dateStr);
    const today = new Date();
    const diffTime = date.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
      return { label: `Dépassé (${Math.abs(diffDays)}j)`, color: "text-rose-400 bg-rose-500/10 border-rose-500/20 animate-pulse" };
    } else if (diffDays <= 30) {
      return { label: `Urgent (${diffDays}j)`, color: "text-amber-400 bg-amber-500/10 border-amber-500/20" };
    } else {
      return { label: `Conforme (${diffDays}j)`, color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20" };
    }
  };

  // 1. LOGIN SCREEN (UNAUTHENTICATED)
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4 font-sans relative overflow-hidden">
        {/* Glow Effects */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-emerald-500/5 rounded-full blur-[100px] pointer-events-none" />

        <MagicCard
          gradientColor="#3b82f622"
          gradientSize={350}
          className="w-full max-w-md border border-slate-800 bg-slate-900/40 backdrop-blur-xl shadow-2xl p-8 rounded-2xl relative"
        >
          <div className="flex flex-col items-center mb-8">
            <div className="h-16 w-16 bg-blue-600/10 border border-blue-500/20 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-blue-500/10">
              <Radio className="h-8 w-8 text-blue-500 animate-pulse" />
            </div>
            <h1 className="text-3xl font-bold tracking-wider text-white font-mono">
              [ <span className="text-blue-500">dolphi</span>SIC ]
            </h1>
            <p className="text-xs text-slate-400 mt-2 font-mono uppercase tracking-widest">
              SDIS 04 • Système de Chiffrement Radio
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-5">
            <div className="space-y-1.5">
              <Label htmlFor="username">Identifiant Agent</Label>
              <div className="relative">
                <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500">
                  <User className="h-4.5 w-4.5" />
                </span>
                <Input
                  id="username"
                  type="text"
                  required
                  placeholder="admin"
                  value={usernameInput}
                  onChange={(e) => setUsernameInput(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="password">Code de Sécurité</Label>
              <div className="relative">
                <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500">
                  <Lock className="h-4.5 w-4.5" />
                </span>
                <Input
                  id="password"
                  type="password"
                  required
                  placeholder="••••••••"
                  value={passwordInput}
                  onChange={(e) => setPasswordInput(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            {authError && (
              <div className="flex items-center gap-2 text-rose-400 bg-rose-500/10 border border-rose-500/20 p-3 rounded-lg text-sm font-mono">
                <AlertTriangle className="h-4 w-4 shrink-0" />
                <span>{authError}</span>
              </div>
            )}

            <PulsatingButton
              type="submit"
              disabled={loading}
              pulseColor="#3b82f6"
              className="w-full mt-4 flex items-center justify-center gap-2 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-mono tracking-wider transition-all disabled:opacity-50"
            >
              {loading ? (
                <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <Unlock className="h-4.5 w-4.5" />
                  <span>DÉVERROUILLER LE SYSTÈME</span>
                </>
              )}
            </PulsatingButton>
          </form>

          <div className="mt-8 pt-6 border-t border-slate-800/80 text-center text-[10px] text-slate-500 font-mono tracking-wide uppercase">
            Accès sécurisé réservé aux agents habilités sdis 04
          </div>
        </MagicCard>
      </div>
    );
  }

  // 2. MAIN APPLICATION (AUTHENTICATED)
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col">
      {/* Top Banner Header */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md sticky top-0 z-40 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 bg-blue-600/10 border border-blue-500/20 rounded-xl flex items-center justify-center shadow-inner">
            <Radio className="h-5 w-5 text-blue-500" />
          </div>
          <div>
            <span className="text-xl font-bold font-mono tracking-wider text-white">
              [ <span className="text-blue-500">dolphi</span>SIC ]
            </span>
            <span className="ml-2 text-[10px] bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full font-mono font-semibold uppercase tracking-wider">
              En ligne
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <div className="text-sm font-semibold text-slate-200 font-mono">{user.username}</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-widest font-mono font-bold">
              {user.role} sdis 04
            </div>
          </div>

          <div className="h-8 w-px bg-slate-800" />

          {/* Settings Button */}
          <button
            onClick={() => setShowSettingsModal(true)}
            className="p-2 hover:bg-slate-800/60 rounded-lg text-slate-400 hover:text-blue-400 transition-colors focus:outline-none"
            title="Paramètres de notifications"
          >
            <Bell className="h-5 w-5" />
          </button>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 py-2 bg-slate-900 border border-slate-800 hover:bg-rose-950/20 hover:border-rose-900/30 text-slate-300 hover:text-rose-400 rounded-lg text-sm font-mono transition-all focus:outline-none"
          >
            <LogOut className="h-4 w-4" />
            <span className="hidden md:inline">Déconnexion</span>
          </button>
        </div>
      </header>

      {/* Main Body */}
      <div className="flex-1 flex flex-col md:flex-row">
        {/* Navigation Sidebar */}
        <aside className="w-full md:w-64 border-r border-slate-800/80 bg-slate-900/20 p-4 space-y-2 flex flex-row md:flex-col overflow-x-auto md:overflow-x-visible">
          <button
            onClick={() => {
              setActiveTab("inventory");
              logUIInteraction("NAVIGATION", "Parc Radio");
            }}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-mono transition-all shrink-0 ${
              activeTab === "inventory"
                ? "bg-blue-600/10 border border-blue-500/30 text-blue-400 font-semibold"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50 border border-transparent"
            }`}
          >
            <Radio className="h-4.5 w-4.5" />
            <span>Parc Radio</span>
          </button>

          <button
            onClick={() => {
              setActiveTab("search");
              logUIInteraction("NAVIGATION", "Recherche");
            }}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-mono transition-all shrink-0 ${
              activeTab === "search"
                ? "bg-blue-600/10 border border-blue-500/30 text-blue-400 font-semibold"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50 border border-transparent"
            }`}
          >
            <Search className="h-4.5 w-4.5" />
            <span>Recherche</span>
          </button>

          <button
            onClick={() => {
              setActiveTab("carto");
              logUIInteraction("NAVIGATION", "Cartographie");
            }}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-mono transition-all shrink-0 ${
              activeTab === "carto"
                ? "bg-blue-600/10 border border-blue-500/30 text-blue-400 font-semibold"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50 border border-transparent"
            }`}
          >
            <MapIcon className="h-4.5 w-4.5" />
            <span>Cartographie</span>
          </button>

          <button
            onClick={() => {
              setActiveTab("stock");
              logUIInteraction("NAVIGATION", "Stocks & Prêts");
            }}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-mono transition-all shrink-0 ${
              activeTab === "stock"
                ? "bg-blue-600/10 border border-blue-500/30 text-blue-400 font-semibold"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50 border border-transparent"
            }`}
          >
            <Package className="h-4.5 w-4.5" />
            <span>Stocks & Prêts</span>
          </button>

          <button
            onClick={() => {
              setActiveTab("stats");
              logUIInteraction("NAVIGATION", "Télémetrie");
            }}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-mono transition-all shrink-0 ${
              activeTab === "stats"
                ? "bg-blue-600/10 border border-blue-500/30 text-blue-400 font-semibold"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50 border border-transparent"
            }`}
          >
            <BarChart3 className="h-4.5 w-4.5" />
            <span>Statistiques</span>
          </button>
        </aside>

        {/* Tab Contents */}
        <main className="flex-1 p-6 overflow-y-auto">
          {/* ==================================================== */}
          {/* 1. TAB: INVENTORY */}
          {/* ==================================================== */}
          {activeTab === "inventory" && (
            <div className="space-y-6">
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-800/60 pb-6">
                <div>
                  <h2 className="text-2xl font-bold text-white tracking-wide flex items-center gap-2">
                    <Radio className="h-6 w-6 text-blue-500" />
                    Gestion du Parc Radio SDIS 04
                  </h2>
                  <p className="text-xs text-slate-400 mt-1 font-mono">
                    Visualisez et configurez les clés de chiffrement de votre flotte opérationnelle.
                  </p>
                </div>

                <div className="flex flex-wrap items-center gap-3">
                  <div className="flex bg-slate-900 border border-slate-800 rounded-lg p-1">
                    {["BIP", "MOBILE", "PORTATIF"].map((t) => (
                      <button
                        key={t}
                        onClick={() => setSelectedType(t)}
                        className={`px-3 py-1.5 rounded-md text-xs font-mono font-semibold uppercase tracking-wider transition-all ${
                          selectedType === t
                            ? "bg-blue-600 text-white shadow-md"
                            : "text-slate-400 hover:text-slate-200"
                        }`}
                      >
                        {t}
                      </button>
                    ))}
                  </div>

                  <select
                    value={selectedCis}
                    onChange={(e) => setSelectedCis(e.target.value)}
                    className="h-10 bg-slate-900 border border-slate-800 rounded-lg px-3 text-sm text-slate-200 font-mono focus:outline-none focus:ring-2 focus:ring-blue-600"
                  >
                    {cisList.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>

                  <Button
                    onClick={() => {
                      setNewDevice({
                        modele: "",
                        num_serie: "",
                        affectation: "",
                        version_logiciel: "",
                        observation: "",
                        date_maj_cle: "",
                      });
                      setShowAddDeviceModal(true);
                    }}
                    className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 border border-emerald-500/20 w-auto"
                  >
                    <Plus className="h-4.5 w-4.5" />
                    <span>Ajouter</span>
                  </Button>
                </div>
              </div>

              {/* Main Panel grid */}
              <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                {/* Devices table list */}
                <div className="xl:col-span-2 space-y-4">
                  <Card className="border-slate-800 bg-slate-900/20 backdrop-blur-sm overflow-hidden">
                    <CardHeader className="bg-slate-900/40 border-b border-slate-800 px-6 py-4">
                      <div className="flex justify-between items-center">
                        <CardTitle className="text-base text-slate-300 font-mono">
                          Équipements déclarés ({devices.length})
                        </CardTitle>
                        <span className="text-[10px] text-slate-500 font-mono uppercase">
                          CIS : {selectedCis} • Type : {selectedType}
                        </span>
                      </div>
                    </CardHeader>
                    <div className="overflow-x-auto">
                      <table className="w-full text-left border-collapse text-slate-300">
                        <thead>
                          <tr className="border-b border-slate-800 bg-slate-900/10 text-xs text-slate-400 font-mono font-bold uppercase tracking-wider">
                            <th className="p-4">Modèle / Marque</th>
                            <th className="p-4">S/N</th>
                            <th className="p-4">Affectation</th>
                            <th className="p-4">Statut Clé</th>
                            <th className="p-4 text-right">Actions</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/40 text-sm">
                          {devices.length === 0 ? (
                            <tr>
                              <td colSpan={5} className="p-8 text-center text-slate-500 font-mono">
                                Aucun équipement trouvé pour ce CIS.
                              </td>
                            </tr>
                          ) : (
                            devices.map((dev) => {
                              const notif = getCryptageStatus(dev.date_cle_a_faire);
                              return (
                                <tr
                                  key={dev.id}
                                  onClick={() => fetchDeviceDetails(dev.id)}
                                  className={`hover:bg-slate-900/40 transition-colors cursor-pointer ${
                                    selectedDevice?.id === dev.id ? "bg-slate-900/60 border-l-2 border-blue-500" : ""
                                  }`}
                                >
                                  <td className="p-4 font-semibold text-white">
                                    {dev.modele}{" "}
                                    {dev.marque && (
                                      <span className="text-[10px] text-slate-500 ml-1 font-mono uppercase bg-slate-950 px-1.5 py-0.5 rounded border border-slate-900">
                                        {dev.marque}
                                      </span>
                                    )}
                                  </td>
                                  <td className="p-4 font-mono text-xs">{dev.num_serie}</td>
                                  <td className="p-4">{dev.affectation || "—"}</td>
                                  <td className="p-4">
                                    <span
                                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono font-semibold border ${notif.color}`}
                                    >
                                      <span className="h-1.5 w-1.5 rounded-full bg-current" />
                                      {notif.label}
                                    </span>
                                  </td>
                                  <td className="p-4 text-right" onClick={(e) => e.stopPropagation()}>
                                    <div className="flex items-center justify-end gap-2">
                                      <button
                                        onClick={() => {
                                          setUpdatingCryptageId(dev.id);
                                          setNewCryptageDate(new Date().toISOString().split("T")[0]);
                                        }}
                                        className="p-1.5 hover:bg-slate-800 rounded border border-slate-800 text-blue-400 hover:text-blue-300 transition-colors"
                                        title="Chiffrement mis à jour"
                                      >
                                        <RefreshCw className="h-4 w-4" />
                                      </button>

                                      <button
                                        onClick={() => handleToggleAlert(dev)}
                                        className={`p-1.5 hover:bg-slate-800 rounded border border-slate-800 transition-colors ${
                                          dev.notification_active ? "text-emerald-400" : "text-slate-500"
                                        }`}
                                        title={dev.notification_active ? "Alerte active" : "Alerte désactivée"}
                                      >
                                        {dev.notification_active ? (
                                          <Bell className="h-4 w-4" />
                                        ) : (
                                          <BellOff className="h-4 w-4" />
                                        )}
                                      </button>

                                      <button
                                        onClick={() => handleDeleteDevice(dev.id)}
                                        className="p-1.5 hover:bg-rose-950/40 rounded border border-slate-800 hover:border-rose-900/30 text-rose-500 hover:text-rose-400 transition-colors"
                                        title="Retirer"
                                      >
                                        <Trash2 className="h-4.5 w-4.5" />
                                      </button>
                                    </div>
                                  </td>
                                </tr>
                              );
                            })
                          )}
                        </tbody>
                      </table>
                    </div>
                  </Card>
                </div>

                {/* Details sidepanel */}
                <div className="space-y-4">
                  {selectedDevice ? (
                    <Card className="border-slate-800 bg-slate-900/40 sticky top-24">
                      <CardHeader className="bg-slate-900/60 border-b border-slate-800 px-6 py-4 flex flex-row items-center justify-between">
                        <div>
                          <CardTitle className="text-lg text-white font-mono">{selectedDevice.modele}</CardTitle>
                          <CardDescription className="text-xs font-mono uppercase">
                            S/N : {selectedDevice.num_serie}
                          </CardDescription>
                        </div>
                        <button
                          onClick={() => setSelectedDevice(null)}
                          className="p-1.5 text-slate-500 hover:text-slate-300 hover:bg-slate-800 rounded-lg focus:outline-none"
                        >
                          <X className="h-4 w-4" />
                        </button>
                      </CardHeader>
                      <CardContent className="p-6 space-y-4 font-mono text-sm">
                        <div className="grid grid-cols-2 gap-y-3 gap-x-4 border-b border-slate-800/80 pb-4 text-xs">
                          <div>
                            <span className="text-slate-500 block">Marque</span>
                            <span className="text-white font-semibold">{selectedDevice.marque || "—"}</span>
                          </div>
                          <div>
                            <span className="text-slate-500 block">Type</span>
                            <span className="text-white font-semibold">{selectedDevice.type || "—"}</span>
                          </div>
                          <div>
                            <span className="text-slate-500 block">CIS d'Affectation</span>
                            <span className="text-white font-semibold">{selectedDevice.cis || "—"}</span>
                          </div>
                          <div>
                            <span className="text-slate-500 block">Affectation Opé</span>
                            <span className="text-white font-semibold">{selectedDevice.affectation || "—"}</span>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-y-3 gap-x-4 border-b border-slate-800/80 pb-4 text-xs">
                          <div>
                            <span className="text-slate-500 block">Clé mise à jour le</span>
                            <span className="text-white font-semibold">
                              {selectedDevice.date_maj_cle
                                ? new Date(selectedDevice.date_maj_cle).toLocaleDateString("fr-FR")
                                : "Jamais"}
                            </span>
                          </div>
                          <div>
                            <span className="text-slate-500 block">Échéance Clé</span>
                            <span className="text-white font-semibold text-blue-400">
                              {selectedDevice.date_cle_a_faire
                                ? new Date(selectedDevice.date_cle_a_faire).toLocaleDateString("fr-FR")
                                : "—"}
                            </span>
                          </div>
                        </div>

                        <div className="space-y-2 text-xs">
                          <h4 className="text-slate-500 uppercase tracking-widest font-semibold">Télémetrie Spécifique</h4>
                          <div className="grid grid-cols-2 gap-2 bg-slate-950 p-3 rounded-lg border border-slate-900 font-mono">
                            {selectedDevice.code_pocsag && (
                              <div>
                                <span className="text-slate-500 text-[10px] block">POCSAG</span>
                                <span className="text-emerald-400 font-semibold">{selectedDevice.code_pocsag}</span>
                              </div>
                            )}
                            {selectedDevice.rfgi && (
                              <div>
                                <span className="text-slate-500 text-[10px] block">RFGI</span>
                                <span className="text-emerald-400 font-semibold">{selectedDevice.rfgi}</span>
                              </div>
                            )}
                            {selectedDevice.immatriculation && (
                              <div>
                                <span className="text-slate-500 text-[10px] block">IMMATRICULATION</span>
                                <span className="text-white font-semibold">{selectedDevice.immatriculation}</span>
                              </div>
                            )}
                            {selectedDevice.version_logiciel && (
                              <div>
                                <span className="text-slate-500 text-[10px] block">VERSION LOGICIEL</span>
                                <span className="text-white font-semibold">{selectedDevice.version_logiciel}</span>
                              </div>
                            )}
                            {selectedDevice.classe_service && (
                              <div>
                                <span className="text-slate-500 text-[10px] block">CLASSE SERVICE</span>
                                <span className="text-white font-semibold">{selectedDevice.classe_service}</span>
                              </div>
                            )}
                            {selectedDevice.date_achat && (
                              <div>
                                <span className="text-slate-500 text-[10px] block">DATE ACHAT</span>
                                <span className="text-white font-semibold">{selectedDevice.date_achat}</span>
                              </div>
                            )}
                          </div>
                        </div>

                        <div className="space-y-1.5 text-xs">
                          <span className="text-slate-500">Observations / Anomalies</span>
                          <div className="bg-slate-950 p-3 rounded-lg border border-slate-900 text-slate-300 min-h-16 text-justify">
                            {selectedDevice.observation || "Aucune observation enregistrée."}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ) : (
                    <Card className="border-slate-800 bg-slate-900/20 border-dashed p-8 text-center text-slate-500 font-mono flex flex-col items-center justify-center min-h-64 sticky top-24">
                      <Info className="h-8 w-8 text-slate-600 mb-3" />
                      Sélectionnez un équipement de la flotte pour afficher son dossier technique détaillé et l'historique de ses configurations de chiffrement.
                    </Card>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* ==================================================== */}
          {/* 2. TAB: SEARCH */}
          {/* ==================================================== */}
          {activeTab === "search" && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white tracking-wide flex items-center gap-2">
                  <Search className="h-6 w-6 text-blue-500" />
                  Recherche Avancée Flotte
                </h2>
                <p className="text-xs text-slate-400 mt-1 font-mono">
                  Effectuez des requêtes croisées sur l'ensemble du parc de télécommunications radio du SDIS 04.
                </p>
              </div>

              <Card className="border-slate-800 bg-slate-900/40 p-6">
                <form onSubmit={handleAdvancedSearch} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="space-y-1">
                    <Label>CIS</Label>
                    <select
                      value={searchForm.cis}
                      onChange={(e) => setSearchForm((prev) => ({ ...prev, cis: e.target.value }))}
                      className="h-10 w-full bg-slate-950 border border-slate-800 rounded-lg px-3 text-sm text-slate-200 font-mono focus:outline-none focus:ring-2 focus:ring-blue-600"
                    >
                      <option value="">Tous les CIS</option>
                      {searchMetadata.centres.map((c) => (
                        <option key={c} value={c}>
                          {c}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-1">
                    <Label>Type</Label>
                    <select
                      value={searchForm.type}
                      onChange={(e) => setSearchForm((prev) => ({ ...prev, type: e.target.value }))}
                      className="h-10 w-full bg-slate-950 border border-slate-800 rounded-lg px-3 text-sm text-slate-200 font-mono focus:outline-none focus:ring-2 focus:ring-blue-600"
                    >
                      <option value="">Tous les Types</option>
                      {searchMetadata.types.map((t) => (
                        <option key={t} value={t}>
                          {t}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-1">
                    <Label>Modèle</Label>
                    <select
                      value={searchForm.modele}
                      onChange={(e) => setSearchForm((prev) => ({ ...prev, modele: e.target.value }))}
                      className="h-10 w-full bg-slate-950 border border-slate-800 rounded-lg px-3 text-sm text-slate-200 font-mono focus:outline-none focus:ring-2 focus:ring-blue-600"
                    >
                      <option value="">Tous les Modèles</option>
                      {searchMetadata.modeles.map((m) => (
                        <option key={m} value={m}>
                          {m}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-1">
                    <Label>Numéro de Série</Label>
                    <Input
                      placeholder="Ex: 5040..."
                      value={searchForm.num_serie}
                      onChange={(e) => setSearchForm((prev) => ({ ...prev, num_serie: e.target.value }))}
                    />
                  </div>

                  <div className="space-y-1">
                    <Label>Affectation opérationnelle</Label>
                    <Input
                      placeholder="Ex: FPT, VSAV..."
                      value={searchForm.affectation}
                      onChange={(e) => setSearchForm((prev) => ({ ...prev, affectation: e.target.value }))}
                    />
                  </div>

                  <div className="space-y-1">
                    <Label>Version logicielle</Label>
                    <Input
                      placeholder="Ex: R05..."
                      value={searchForm.version_logiciel}
                      onChange={(e) => setSearchForm((prev) => ({ ...prev, version_logiciel: e.target.value }))}
                    />
                  </div>

                  <div className="space-y-1 md:col-span-2">
                    <Label>Observations</Label>
                    <Input
                      placeholder="Mot-clé d'observation..."
                      value={searchForm.observation}
                      onChange={(e) => setSearchForm((prev) => ({ ...prev, observation: e.target.value }))}
                    />
                  </div>

                  <div className="md:col-span-2 lg:col-span-4 flex justify-end gap-3 pt-2">
                    <button
                      type="button"
                      onClick={() => {
                        setSearchForm({
                          cis: "",
                          modele: "",
                          type: "",
                          num_serie: "",
                          affectation: "",
                          observation: "",
                          version_logiciel: "",
                        });
                        setSearchResults([]);
                      }}
                      className="px-4 py-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 rounded-lg text-sm font-mono transition-colors focus:outline-none"
                    >
                      Réinitialiser
                    </button>
                    <button
                      type="submit"
                      className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-mono tracking-wider transition-colors focus:outline-none shadow-lg shadow-blue-500/10"
                    >
                      Lancer la Recherche
                    </button>
                  </div>
                </form>
              </Card>

              {searchResults.length > 0 && (
                <Card className="border-slate-800 bg-slate-900/20 overflow-hidden">
                  <CardHeader className="bg-slate-900/40 border-b border-slate-800 px-6 py-4">
                    <CardTitle className="text-base text-slate-300 font-mono">
                      Résultats de la recherche ({searchResults.length})
                    </CardTitle>
                  </CardHeader>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse text-slate-300">
                      <thead>
                        <tr className="border-b border-slate-800 bg-slate-900/10 text-xs text-slate-400 font-mono font-bold uppercase tracking-wider">
                          <th className="p-4">CIS</th>
                          <th className="p-4">Modèle / Type</th>
                          <th className="p-4">S/N</th>
                          <th className="p-4">Affectation</th>
                          <th className="p-4">Clé de Chiffrement</th>
                          <th className="p-4 text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/40 text-sm">
                        {searchResults.map((dev) => {
                          const status = getCryptageStatus(dev.date_cle_a_faire);
                          return (
                            <tr key={dev.id} className="hover:bg-slate-900/40 transition-colors">
                              <td className="p-4 font-mono font-semibold text-slate-200">{dev.cis}</td>
                              <td className="p-4">
                                <span className="font-semibold text-white">{dev.modele}</span>
                                <span className="text-[10px] text-slate-500 ml-1.5 font-mono uppercase bg-slate-950 px-1.5 py-0.5 rounded border border-slate-900">
                                  {dev.type}
                                </span>
                              </td>
                              <td className="p-4 font-mono text-xs">{dev.num_serie}</td>
                              <td className="p-4">{dev.affectation || "—"}</td>
                              <td className="p-4">
                                <span
                                  className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono font-semibold border ${status.color}`}
                                >
                                  <span className="h-1.5 w-1.5 rounded-full bg-current" />
                                  {status.label}
                                </span>
                              </td>
                              <td className="p-4 text-right">
                                <div className="flex items-center justify-end gap-2">
                                  <button
                                    onClick={() => {
                                      setSelectedCis(dev.cis);
                                      setSelectedType(dev.type);
                                      setSelectedDevice(dev);
                                      setActiveTab("inventory");
                                    }}
                                    className="px-2.5 py-1 text-xs bg-slate-900 border border-slate-800 hover:bg-slate-800 text-blue-400 hover:text-blue-300 rounded font-mono transition-colors"
                                  >
                                    Inspecter
                                  </button>
                                </div>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </Card>
              )}
            </div>
          )}

          {/* ==================================================== */}
          {/* 3. TAB: CARTOGRAPHY */}
          {/* ==================================================== */}
          {activeTab === "carto" && (
            <div className="h-[calc(100vh-120px)] flex flex-col lg:flex-row gap-6 relative">
              {/* Map view container */}
              <div className="flex-1 flex flex-col gap-4">
                <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900/60 border border-slate-800 px-4 py-2.5 rounded-xl">
                  <div className="flex items-center gap-3">
                    <MapIcon className="h-5 w-5 text-blue-500 animate-pulse" />
                    <span className="font-semibold text-white font-mono text-sm">Cartographie Opérationnelle</span>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className="text-xs text-slate-400 font-mono">Mode d'Action :</span>
                    <select
                      id="map-mode-selector"
                      value={mapMode}
                      onChange={(e) => {
                        setMapMode(e.target.value as any);
                        logUIInteraction("CHANGE", "Mode carte", { mode: e.target.value });
                      }}
                      className="bg-slate-950 border border-slate-800 text-xs text-slate-200 font-mono rounded px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-600"
                    >
                      <option value="view">Navigation (Consultation)</option>
                      <option value="add_site">Ajouter un Site (Clic Carte)</option>
                      <option value="add_label">Ajouter un Label Libre (Clic Carte)</option>
                      <option value="add_liaison">Ajouter Liaison (Clic Site A puis B)</option>
                    </select>

                    <input type="hidden" id="liaison-first-site" value="" />
                  </div>
                </div>

                {/* Map Div */}
                <div ref={mapContainerRef} className="flex-1 min-h-[450px] rounded-xl overflow-hidden relative shadow-lg border border-slate-800/80" />
              </div>

              {/* Sidebar Info Drawer */}
              {(selectedSite || selectedLiaison) && (
                <div className="w-full lg:w-[410px] bg-slate-900 border border-slate-800 rounded-xl flex flex-col shrink-0 overflow-hidden shadow-2xl relative">
                  {/* Header */}
                  <div className="p-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-2 max-w-[70%]">
                      {selectedSite ? (
                        <>
                          <MapPin className="h-4.5 w-4.5 text-blue-500 shrink-0" />
                          <h3 className="font-mono text-sm font-bold text-white truncate" title={selectedSite.nom}>
                            {selectedSite.nom}
                          </h3>
                        </>
                      ) : (
                        <>
                          <Activity className="h-4.5 w-4.5 text-emerald-500 shrink-0" />
                          <h3 className="font-mono text-sm font-bold text-white truncate" title={selectedLiaison.label || "Liaison"}>
                            Liaison : {selectedLiaison.label || "Faisceau"}
                          </h3>
                        </>
                      )}
                    </div>

                    <div className="flex items-center gap-2">
                      {/* Delete Global */}
                      <button
                        onClick={() =>
                          selectedSite ? handleDeleteSite(selectedSite.id) : handleDeleteLiaison(selectedLiaison.id)
                        }
                        className="p-1.5 hover:bg-rose-950/40 rounded border border-slate-800 hover:border-rose-900/30 text-rose-500 hover:text-rose-400 transition-colors focus:outline-none"
                        title={selectedSite ? "Supprimer le Site" : "Supprimer la Liaison"}
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>

                      <button
                        onClick={() => {
                          setSelectedSite(null);
                          setSelectedLiaison(null);
                        }}
                        className="p-1.5 text-slate-500 hover:text-slate-300 hover:bg-slate-800 rounded-lg focus:outline-none"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  {/* Site Tabs and contents */}
                  {selectedSite ? (
                    <div className="flex-1 flex flex-col min-h-0">
                      {/* Horizontal tab list - custom fine scrollbar */}
                      <div className="flex bg-slate-950 border-b border-slate-800/80 px-2 py-1 gap-1 overflow-x-auto select-none no-scrollbar">
                        {[
                          { id: "inventaire", label: "Inventaire" },
                          { id: "taches", label: "Tâches" },
                          { id: "pylones", label: "Pylônes" },
                          { id: "log", label: "Log" },
                          { id: "documents", label: "Docs" },
                        ].map((tab) => (
                          <button
                            key={tab.id}
                            onClick={() => setActiveSiteTab(tab.id as any)}
                            className={`px-3 py-1.5 rounded-md text-xs font-mono font-semibold transition-all shrink-0 ${
                              activeSiteTab === tab.id
                                ? "bg-blue-600/10 text-blue-400 border border-blue-500/20"
                                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50"
                            }`}
                          >
                            {tab.label}
                          </button>
                        ))}
                      </div>

                      {/* Tab content area */}
                      <div className="flex-1 p-4 overflow-y-auto space-y-4">
                        {/* 1. Inventaire */}
                        {activeSiteTab === "inventaire" && (
                          <div className="space-y-3">
                            <Label>Inventaire du matériel sur site</Label>
                            <textarea
                              value={siteInfo.inventaire}
                              onChange={(e) => setSiteInfo((prev) => ({ ...prev, inventaire: e.target.value }))}
                              placeholder="Liste du matériel présent (Ex: Antennes, Baies, Émetteurs...)"
                              className="w-full h-72 bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-300 font-mono focus:outline-none focus:ring-1 focus:ring-blue-600 resize-none"
                            />
                            <button
                              onClick={saveSiteInfo}
                              className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-mono font-bold transition-colors"
                            >
                              Enregistrer l'Inventaire
                            </button>
                          </div>
                        )}

                        {/* 2. Tâches */}
                        {activeSiteTab === "taches" && (
                          <div className="space-y-3">
                            <Label>Fiche de tâches et travaux</Label>
                            <textarea
                              value={siteInfo.taches}
                              onChange={(e) => setSiteInfo((prev) => ({ ...prev, taches: e.target.value }))}
                              placeholder="Travaux à réaliser, maintenances périodiques, comptes-rendus..."
                              className="w-full h-72 bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-300 font-mono focus:outline-none focus:ring-1 focus:ring-blue-600 resize-none"
                            />
                            <button
                              onClick={saveSiteInfo}
                              className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-mono font-bold transition-colors"
                            >
                              Enregistrer les Tâches
                            </button>
                          </div>
                        )}

                        {/* 3. Pylones */}
                        {activeSiteTab === "pylones" && (
                          <div className="space-y-4">
                            <form onSubmit={handleAddPylone} className="space-y-2 border-b border-slate-800/80 pb-3">
                              <Input
                                placeholder="Nom du pylône (Ex: Pylône Est)"
                                required
                                value={newPyloneName}
                                onChange={(e) => setNewPyloneName(e.target.value)}
                                className="h-8 text-xs"
                              />
                              <Input
                                placeholder="Description (Ex: Hauteur 15m, Haubané)"
                                value={newPyloneDesc}
                                onChange={(e) => setNewPyloneDesc(e.target.value)}
                                className="h-8 text-xs"
                              />
                              <button
                                type="submit"
                                className="w-full py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-mono font-bold transition-colors"
                              >
                                Ajouter Pylône
                              </button>
                            </form>

                            <div className="space-y-2 max-h-60 overflow-y-auto">
                              {pylones.length === 0 ? (
                                <div className="text-center text-slate-500 text-xs font-mono py-4">
                                  Aucun pylône déclaré.
                                </div>
                              ) : (
                                pylones.map((p) => (
                                  <div
                                    key={p.id}
                                    className="flex justify-between items-start bg-slate-950 p-2.5 rounded border border-slate-900 text-xs font-mono"
                                  >
                                    <div className="max-w-[80%]">
                                      <div className="font-bold text-white">{p.nom_pylone}</div>
                                      <div className="text-slate-400 mt-1 text-[11px]">{p.description || "Pas de description"}</div>
                                    </div>
                                    <button
                                      onClick={() => handleDeletePylone(p.id)}
                                      className="text-rose-500 hover:text-rose-400 p-0.5 focus:outline-none"
                                    >
                                      <Trash2 className="h-4 w-4" />
                                    </button>
                                  </div>
                                ))
                              )}
                            </div>
                          </div>
                        )}

                        {/* 4. Log (Main Courante) */}
                        {activeSiteTab === "log" && (
                          <div className="space-y-4">
                            <form onSubmit={handleAddEvent} className="flex gap-2">
                              <Input
                                placeholder="Nouvel événement..."
                                required
                                value={newEventText}
                                onChange={(e) => setNewEventText(e.target.value)}
                                className="h-9 text-xs flex-1"
                              />
                              <button
                                type="submit"
                                className="px-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-mono font-bold transition-colors"
                              >
                                Enregistrer
                              </button>
                            </form>

                            <div className="space-y-2 max-h-72 overflow-y-auto divide-y divide-slate-800/40">
                              {mainCourante.length === 0 ? (
                                <div className="text-center text-slate-500 text-xs font-mono py-4">
                                  Historique vide.
                                </div>
                              ) : (
                                mainCourante.map((item) => (
                                  <div key={item.id} className="pt-2 pb-1.5 text-xs font-mono">
                                    <div className="flex items-center justify-between text-slate-400 text-[10px] mb-1">
                                      <span className="flex items-center gap-1.5">
                                        <Clock className="h-3 w-3" />
                                        {item.date_heure}
                                      </span>
                                      <button
                                        onClick={() => handleDeleteEvent(item.id)}
                                        className="text-rose-500 hover:text-rose-400 p-0.5 focus:outline-none"
                                      >
                                        ✕
                                      </button>
                                    </div>
                                    <p className="text-slate-200 leading-normal">{item.evenement}</p>
                                  </div>
                                ))
                              )}
                            </div>
                          </div>
                        )}

                        {/* 5. Documents */}
                        {activeSiteTab === "documents" && (
                          <div className="space-y-4">
                            <form onSubmit={handleFileUpload} className="space-y-2 border-b border-slate-800/80 pb-3">
                              <Label htmlFor="file-upload-input" className="text-xs">Joindre un document (Image, PDF)</Label>
                              <div className="flex gap-2">
                                <input
                                  type="file"
                                  id="file-upload-input"
                                  onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                                  className="w-full text-xs text-slate-400 file:mr-2.5 file:py-1 file:px-2.5 file:rounded file:border-0 file:text-[11px] file:font-mono file:bg-slate-800 file:text-slate-300 hover:file:bg-slate-700 bg-slate-950 border border-slate-800 rounded p-1.5"
                                />
                                <button
                                  type="submit"
                                  disabled={!uploadFile}
                                  className="px-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-mono font-bold transition-colors disabled:opacity-50 disabled:pointer-events-none"
                                >
                                  <Upload className="h-4 w-4" />
                                </button>
                              </div>
                            </form>

                            <div className="space-y-2 max-h-60 overflow-y-auto">
                              {documents.length === 0 ? (
                                <div className="text-center text-slate-500 text-xs font-mono py-4">
                                  Aucun document rattaché.
                                </div>
                              ) : (
                                documents.map((doc) => (
                                  <div
                                    key={doc.id}
                                    className="flex justify-between items-center bg-slate-950 p-2 border border-slate-900 rounded text-xs font-mono"
                                  >
                                    <span className="text-slate-300 truncate max-w-[65%]" title={doc.nom_fichier}>
                                      {doc.nom_fichier}
                                    </span>
                                    <div className="flex gap-2.5">
                                      <a
                                        href={`/api/carto/documents/${doc.id}/download`}
                                        className="text-blue-400 hover:text-blue-300 p-0.5"
                                        title="Télécharger"
                                      >
                                        <Download className="h-4 w-4" />
                                      </a>
                                      <button
                                        onClick={() => handleDeleteDocument(doc.id)}
                                        className="text-rose-500 hover:text-rose-400 p-0.5 focus:outline-none"
                                        title="Supprimer"
                                      >
                                        <Trash2 className="h-4 w-4" />
                                      </button>
                                    </div>
                                  </div>
                                ))
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ) : (
                    /* Liaison Info */
                    <div className="flex-1 p-4 space-y-4">
                      <div className="space-y-1.5 font-mono text-xs text-slate-400">
                        <div>
                          <span className="text-slate-500 font-bold uppercase">Origine (A) :</span>{" "}
                          <span className="text-slate-200">{selectedLiaison.nom_a}</span>
                        </div>
                        <div>
                          <span className="text-slate-500 font-bold uppercase">Destination (B) :</span>{" "}
                          <span className="text-slate-200">{selectedLiaison.nom_b}</span>
                        </div>
                        <div>
                          <span className="text-slate-500 font-bold uppercase">Couleur Traceur :</span>{" "}
                          <span
                            className="inline-block h-3.5 w-3.5 rounded border border-slate-700 align-middle ml-1.5"
                            style={{ backgroundColor: selectedLiaison.couleur }}
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label>Notes techniques sur la liaison radio</Label>
                        <textarea
                          id={`liaison-notes-${selectedLiaison.id}`}
                          defaultValue={selectedLiaison.notes || ""}
                          placeholder="Informations sur la fréquence, le type de multiplexage, les canaux d'écoute..."
                          className="w-full h-60 bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-300 font-mono focus:outline-none focus:ring-1 focus:ring-blue-600 resize-none"
                        />
                        <button
                          onClick={() => {
                            const val = (document.getElementById(`liaison-notes-${selectedLiaison.id}`) as HTMLTextAreaElement).value;
                            saveLiaisonNotes(selectedLiaison.id, val);
                          }}
                          className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-mono font-bold transition-colors"
                        >
                          Enregistrer les Notes
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* ==================================================== */}
          {/* 4. TAB: STOCK & LOANS */}
          {/* ==================================================== */}
          {activeTab === "stock" && (
            <div className="space-y-6">
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-800/60 pb-6">
                <div>
                  <h2 className="text-2xl font-bold text-white tracking-wide flex items-center gap-2">
                    <Package className="h-6 w-6 text-blue-500" />
                    Stocks & Prêts Matériel
                  </h2>
                  <p className="text-xs text-slate-400 mt-1 font-mono">
                    Gérez le parc de réserve opérationnel et suivez les affectations temporaires (prêts).
                  </p>
                </div>

                <div>
                  <Button
                    onClick={() => {
                      setNewStockItem({
                        nom: "",
                        description: "",
                        type_materiel: "BIP",
                        etat: "Neuf",
                        modele: "",
                        num_serie: "",
                        cis: "",
                        pocsag: "",
                        rfgi: "",
                        identifiant: "",
                      });
                      setShowAddStockModal(true);
                    }}
                    className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 border border-emerald-500/20 w-auto"
                  >
                    <Plus className="h-4.5 w-4.5" />
                    <span>Ajouter au Stock</span>
                  </Button>
                </div>
              </div>

              {/* Stock dashboard grid */}
              <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                {/* Stock table list */}
                <div className="xl:col-span-2 space-y-4">
                  <Card className="border-slate-800 bg-slate-900/20 overflow-hidden">
                    <CardHeader className="bg-slate-900/40 border-b border-slate-800 px-6 py-4">
                      <CardTitle className="text-base text-slate-300 font-mono">
                        Inventaire de réserve ({stockItems.length})
                      </CardTitle>
                    </CardHeader>
                    <div className="overflow-x-auto">
                      <table className="w-full text-left border-collapse text-slate-300">
                        <thead>
                          <tr className="border-b border-slate-800 bg-slate-900/10 text-xs text-slate-400 font-mono font-bold uppercase tracking-wider">
                            <th className="p-4">Matériel / Modèle</th>
                            <th className="p-4">Catégorie</th>
                            <th className="p-4">État</th>
                            <th className="p-4">Disponibilité</th>
                            <th className="p-4 text-right">Actions</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/40 text-sm">
                          {stockItems.length === 0 ? (
                            <tr>
                              <td colSpan={5} className="p-8 text-center text-slate-500 font-mono">
                                Aucun matériel dans la réserve.
                              </td>
                            </tr>
                          ) : (
                            stockItems.map((item) => (
                              <tr
                                key={item.id}
                                onClick={() => {
                                  setSelectedStockItem(item);
                                  fetchLoanHistory(item.id);
                                }}
                                className={`hover:bg-slate-900/40 transition-colors cursor-pointer ${
                                  selectedStockItem?.id === item.id ? "bg-slate-900/60 border-l-2 border-blue-500" : ""
                                }`}
                              >
                                <td className="p-4 font-semibold text-white">
                                  {item.nom}{" "}
                                  {item.num_serie && (
                                    <span className="text-[10px] text-slate-500 font-mono bg-slate-950 px-1.5 py-0.5 rounded border border-slate-900 ml-1">
                                      S/N: {item.num_serie}
                                    </span>
                                  )}
                                </td>
                                <td className="p-4 font-mono text-xs">{item.type_materiel}</td>
                                <td className="p-4 text-xs font-mono">{item.etat}</td>
                                <td className="p-4 text-xs">
                                  {item.statut === "Disponible" ? (
                                    <span className="inline-flex items-center gap-1.5 px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-full font-semibold font-mono">
                                      Disponible
                                    </span>
                                  ) : (
                                    <span className="inline-flex items-center gap-1.5 px-2 py-0.5 bg-blue-500/10 border border-blue-500/20 text-blue-400 rounded-full font-semibold font-mono">
                                      Prêté à {item.emprunteur}
                                    </span>
                                  )}
                                </td>
                                <td className="p-4 text-right" onClick={(e) => e.stopPropagation()}>
                                  <div className="flex justify-end gap-2">
                                    {item.statut === "Disponible" ? (
                                      <button
                                        onClick={() => {
                                          setShowLoanModal(item);
                                          setLoanForm({
                                            emprunteur: "",
                                            date_debut: new Date().toISOString().split("T")[0],
                                            date_fin: "",
                                          });
                                        }}
                                        className="px-2.5 py-1 text-xs bg-blue-600 hover:bg-blue-500 text-white rounded font-mono transition-colors"
                                      >
                                        Prêter
                                      </button>
                                    ) : (
                                      <button
                                        onClick={() => {
                                          setShowReturnModal(item);
                                          setReturnForm({ changement_etat: "", nouveau_statut_etat: item.etat });
                                        }}
                                        className="px-2.5 py-1 text-xs bg-emerald-600 hover:bg-emerald-500 text-white rounded font-mono transition-colors"
                                      >
                                        Retour
                                      </button>
                                    )}

                                    <button
                                      onClick={() => handleDeleteStock(item.id)}
                                      className="p-1 hover:bg-rose-950/40 rounded border border-slate-800 hover:border-rose-900/30 text-rose-500 hover:text-rose-400 transition-colors"
                                      title="Supprimer définitivement"
                                    >
                                      <Trash2 className="h-4.5 w-4.5" />
                                    </button>
                                  </div>
                                </td>
                              </tr>
                            ))
                          )}
                        </tbody>
                      </table>
                    </div>
                  </Card>
                </div>

                {/* Selected stock item details & loan history */}
                <div className="space-y-4">
                  {selectedStockItem ? (
                    <Card className="border-slate-800 bg-slate-900/40 sticky top-24">
                      <CardHeader className="bg-slate-900/60 border-b border-slate-800 px-6 py-4 flex flex-row items-center justify-between">
                        <div>
                          <CardTitle className="text-base text-white font-mono">{selectedStockItem.nom}</CardTitle>
                          <CardDescription className="text-xs font-mono uppercase">
                            Catégorie : {selectedStockItem.type_materiel}
                          </CardDescription>
                        </div>
                        <button
                          onClick={() => setSelectedStockItem(null)}
                          className="p-1 text-slate-500 hover:text-slate-300 hover:bg-slate-800 rounded-lg focus:outline-none"
                        >
                          <X className="h-4 w-4" />
                        </button>
                      </CardHeader>
                      <CardContent className="p-6 space-y-4 text-xs font-mono">
                        <div className="space-y-1 bg-slate-950 p-3 rounded-lg border border-slate-900 font-mono">
                          <div>
                            <span className="text-slate-500">Description :</span>
                            <p className="text-slate-200 mt-1">{selectedStockItem.description || "Aucune description"}</p>
                          </div>
                        </div>

                        {/* Extra technical fields if present */}
                        <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-400 border-b border-slate-800/80 pb-3">
                          {selectedStockItem.num_serie && (
                            <div>
                              <span className="text-slate-500 block">N° SÉRIE</span>
                              <span className="text-slate-200 font-semibold">{selectedStockItem.num_serie}</span>
                            </div>
                          )}
                          {selectedStockItem.cis && (
                            <div>
                              <span className="text-slate-500 block">CIS ORIGINE</span>
                              <span className="text-slate-200 font-semibold">{selectedStockItem.cis}</span>
                            </div>
                          )}
                          {selectedStockItem.pocsag && (
                            <div>
                              <span className="text-slate-500 block">POCSAG</span>
                              <span className="text-emerald-400 font-semibold">{selectedStockItem.pocsag}</span>
                            </div>
                          )}
                          {selectedStockItem.rfgi && (
                            <div>
                              <span className="text-slate-500 block">RFGI (ANTARES)</span>
                              <span className="text-emerald-400 font-semibold">{selectedStockItem.rfgi}</span>
                            </div>
                          )}
                          {selectedStockItem.identifiant && (
                            <div>
                              <span className="text-slate-500 block">IDENTIFIANT</span>
                              <span className="text-emerald-400 font-semibold">{selectedStockItem.identifiant}</span>
                            </div>
                          )}
                        </div>

                        {/* Loan details */}
                        <div className="space-y-3 pt-2">
                          <h4 className="text-slate-500 font-bold uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                            <Clock className="h-3.5 w-3.5" />
                            Historique des mouvements
                          </h4>

                          <div className="space-y-2 max-h-64 overflow-y-auto divide-y divide-slate-800/40">
                            {stockHistory.length === 0 ? (
                              <div className="text-center text-slate-600 py-4">
                                Aucun mouvement enregistré pour ce matériel.
                              </div>
                            ) : (
                              stockHistory.map((h) => (
                                <div key={h.id} className="pt-2 pb-1 text-[11px]">
                                  <div className="flex justify-between items-center text-slate-300 font-bold mb-1">
                                    <span className="flex items-center gap-1">
                                      <User className="h-3 w-3" />
                                      {h.emprunteur}
                                    </span>
                                    {h.date_rendu ? (
                                      <span className="text-[10px] px-1.5 py-0.5 bg-emerald-500/15 border border-emerald-500/10 text-emerald-400 rounded-sm">
                                        Rendu le {new Date(h.date_rendu).toLocaleDateString("fr-FR")}
                                      </span>
                                    ) : (
                                      <span className="text-[10px] px-1.5 py-0.5 bg-blue-500/15 border border-blue-500/10 text-blue-400 rounded-sm animate-pulse">
                                        En cours
                                      </span>
                                    )}
                                  </div>
                                  <div className="text-slate-500 flex justify-between">
                                    <span>
                                      Du {new Date(h.date_debut).toLocaleDateString("fr-FR")} au{" "}
                                      {new Date(h.date_fin).toLocaleDateString("fr-FR")}
                                    </span>
                                  </div>
                                  {h.changement_etat && (
                                    <div className="text-[10px] text-amber-500 mt-1 italic">
                                      Note de retour : {h.changement_etat}
                                    </div>
                                  )}
                                </div>
                              ))
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ) : (
                    <Card className="border-slate-800 bg-slate-900/20 border-dashed p-8 text-center text-slate-500 font-mono flex flex-col items-center justify-center min-h-64 sticky top-24">
                      <Info className="h-8 w-8 text-slate-600 mb-3" />
                      Sélectionnez un matériel pour inspecter ses caractéristiques et son historique d'emprunt.
                    </Card>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* ==================================================== */}
          {/* 5. TAB: STATISTICS & TELEMETRY */}
          {/* ==================================================== */}
          {activeTab === "stats" && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white tracking-wide flex items-center gap-2">
                  <BarChart3 className="h-6 w-6 text-blue-500" />
                  Tableau de Bord Télémétrique Flotte
                </h2>
                <p className="text-xs text-slate-400 mt-1 font-mono">
                  Consultez la distribution et l'état de l'ensemble du parc radio SDIS 04 en temps réel.
                </p>
              </div>

              {/* Stats KPI cards */}
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
                <Card className="border-slate-800 bg-slate-900/40 p-5 flex flex-col items-center text-center">
                  <span className="text-[10px] text-slate-500 uppercase tracking-widest font-mono font-bold">
                    Équipements Totaux
                  </span>
                  <span className="text-3xl font-bold font-mono text-white mt-2">
                    {statsData.total_equipments}
                  </span>
                </Card>

                {/* Calculate types counts directly from type array */}
                {["BIP", "MOBILE", "PORTATIF"].map((type) => {
                  const count = statsData.by_type.find((x: any) => x.type === type)?.count || 0;
                  return (
                    <Card key={type} className="border-slate-800 bg-slate-900/40 p-5 flex flex-col items-center text-center">
                      <span className="text-[10px] text-slate-500 uppercase tracking-widest font-mono font-bold">
                        Flotte {type}
                      </span>
                      <span className="text-3xl font-bold font-mono text-blue-400 mt-2">{count}</span>
                    </Card>
                  );
                })}
              </div>

              {/* CSS Graphs Panels */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 1. Count by Type */}
                <Card className="border-slate-800 bg-slate-900/40 p-6 space-y-4">
                  <h3 className="text-sm font-bold uppercase tracking-widest font-mono text-slate-300">
                    Répartition par Catégorie de Flotte
                  </h3>
                  <div className="space-y-3.5">
                    {statsData.by_type.map((t: any) => {
                      const percentage = statsData.total_equipments
                        ? Math.round((t.count / statsData.total_equipments) * 100)
                        : 0;
                      return (
                        <div key={t.type} className="space-y-1 text-xs font-mono">
                          <div className="flex justify-between text-slate-300">
                            <span>{t.type}</span>
                            <span>
                              {t.count} ({percentage}%)
                            </span>
                          </div>
                          <div className="h-3 w-full bg-slate-950 rounded-full border border-slate-900 overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-blue-600 to-blue-400 rounded-full shadow-inner shadow-blue-500/50"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </Card>

                {/* 2. Count by Top Models */}
                <Card className="border-slate-800 bg-slate-900/40 p-6 space-y-4">
                  <h3 className="text-sm font-bold uppercase tracking-widest font-mono text-slate-300">
                    Top 6 Modèles les Plus Représentés
                  </h3>
                  <div className="space-y-3.5">
                    {statsData.by_model.slice(0, 6).map((m: any) => {
                      const maxVal = statsData.by_model[0]?.count || 1;
                      const percentage = Math.round((m.count / maxVal) * 100);
                      return (
                        <div key={m.modele} className="space-y-1 text-xs font-mono">
                          <div className="flex justify-between text-slate-300">
                            <span className="truncate max-w-[65%]">
                              {m.modele} <span className="text-[10px] text-slate-500">({m.type})</span>
                            </span>
                            <span>{m.count}</span>
                          </div>
                          <div className="h-3 w-full bg-slate-950 rounded-full border border-slate-900 overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-emerald-600 to-emerald-400 rounded-full shadow-inner"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </Card>

                {/* 3. Distribution by Center (Top 10) */}
                <Card className="border-slate-800 bg-slate-900/40 p-6 space-y-4 lg:col-span-2">
                  <h3 className="text-sm font-bold uppercase tracking-widest font-mono text-slate-300">
                    Densité de Flotte par CIS (Top 10)
                  </h3>
                  <div className="space-y-3.5">
                    {statsData.by_centre.slice(0, 10).map((c: any) => {
                      const maxVal = statsData.by_centre[0]?.count || 1;
                      const percentage = Math.round((c.count / maxVal) * 100);
                      return (
                        <div key={c.cis} className="space-y-1 text-xs font-mono">
                          <div className="flex justify-between text-slate-300">
                            <span>{c.cis}</span>
                            <span>{c.count} équipements</span>
                          </div>
                          <div className="h-3 w-full bg-slate-950 rounded-full border border-slate-900 overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-blue-600 to-emerald-500 rounded-full shadow-inner"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </Card>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* ==================================================== */}
      {/* GLOBAL MODALS AND OVERLAYS */}
      {/* ==================================================== */}

      {/* 1. NOTIFICATIONS SETTINGS MODAL */}
      {showSettingsModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md max-h-[90vh] overflow-y-auto border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <Bell className="h-5 w-5 text-blue-500 animate-bounce" />
                Alertes Chiffrement
              </CardTitle>
              <button
                onClick={() => setShowSettingsModal(false)}
                className="text-slate-500 hover:text-slate-300 focus:outline-none"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4 text-sm font-mono">
              <div className="flex items-center justify-between">
                <Label htmlFor="global-notif-toggle">Activer les alertes globales</Label>
                <input
                  id="global-notif-toggle"
                  type="checkbox"
                  checked={notifSettings.global_notification_enabled}
                  onChange={(e) =>
                    setNotifSettings((prev) => ({ ...prev, global_notification_enabled: e.target.checked }))
                  }
                  className="h-4.5 w-4.5 accent-blue-600"
                />
              </div>

              <div className="flex items-center justify-between">
                <Label htmlFor="notif-exceeded-toggle">Alerte clé dépassée (échéance passée)</Label>
                <input
                  id="notif-exceeded-toggle"
                  type="checkbox"
                  checked={notifSettings.notify_exceeded}
                  onChange={(e) => setNotifSettings((prev) => ({ ...prev, notify_exceeded: e.target.checked }))}
                  className="h-4.5 w-4.5 accent-blue-600"
                />
              </div>

              <div className="flex items-center justify-between">
                <Label htmlFor="notif-approaching-toggle">Alerte clé approchante (échéance &lt; 30j)</Label>
                <input
                  id="notif-approaching-toggle"
                  type="checkbox"
                  checked={notifSettings.notify_approaching}
                  onChange={(e) => setNotifSettings((prev) => ({ ...prev, notify_approaching: e.target.checked }))}
                  className="h-4.5 w-4.5 accent-blue-600"
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="notif-email">Adresse e-mail d'envoi</Label>
                <Input
                  id="notif-email"
                  type="email"
                  placeholder="transmissions@sdis04.fr"
                  value={notifSettings.email_notif}
                  onChange={(e) => setNotifSettings((prev) => ({ ...prev, email_notif: e.target.value }))}
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
              <button
                onClick={() => setShowSettingsModal(false)}
                className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 font-mono transition-colors"
              >
                Annuler
              </button>
              <button
                onClick={saveNotificationSettings}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs rounded font-mono font-bold transition-colors"
              >
                Enregistrer
              </button>
            </div>
          </Card>
        </div>
      )}

      {/* 2. UPDATE CRYPTAGE DATE MODAL */}
      {updatingCryptageId !== null && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-sm border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <FileCheck className="h-5 w-5 text-blue-500" />
                Date de Cryptage
              </CardTitle>
              <button
                onClick={() => setUpdatingCryptageId(null)}
                className="text-slate-500 hover:text-slate-300 focus:outline-none"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleUpdateCryptage} className="space-y-4">
              <div className="space-y-1.5">
                <Label htmlFor="date-cryptage-input">Date de la mise à jour de la clé</Label>
                <Input
                  id="date-cryptage-input"
                  type="date"
                  required
                  value={newCryptageDate}
                  onChange={(e) => setNewCryptageDate(e.target.value)}
                />
                <p className="text-[10px] text-slate-500 font-mono italic">
                  Note : La date d'échéance de la clé sera automatiquement projetée à +2 ans.
                </p>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setUpdatingCryptageId(null)}
                  className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 font-mono transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs rounded font-mono font-bold transition-colors"
                >
                  Valider
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}

      {/* 3. ADD DEVICE TO PARC MODAL */}
      {showAddDeviceModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <Plus className="h-5 w-5 text-emerald-500" />
                Ajouter un Équipement au Parc
              </CardTitle>
              <button
                onClick={() => setShowAddDeviceModal(false)}
                className="text-slate-500 hover:text-slate-300 focus:outline-none"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddDevice} className="space-y-4 font-mono text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5 col-span-2">
                  <Label>Modèle du matériel (Référentiel)</Label>
                  <select
                    value={newDevice.modele}
                    onChange={(e) => setNewDevice((prev) => ({ ...prev, modele: e.target.value }))}
                    className="h-10 w-full bg-slate-950 border border-slate-800 rounded-lg px-3 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600"
                  >
                    {availableModels.map((m) => (
                      <option key={m} value={m}>
                        {m}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="add-sn">Numéro de Série (S/N)</Label>
                  <Input
                    id="add-sn"
                    required
                    placeholder="S/N matériel..."
                    value={newDevice.num_serie}
                    onChange={(e) => setNewDevice((prev) => ({ ...prev, num_serie: e.target.value }))}
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="add-affectation">Affectation opérationnelle</Label>
                  <Input
                    id="add-affectation"
                    placeholder="Ex: FPT 1, VSAV 2..."
                    value={newDevice.affectation}
                    onChange={(e) => setNewDevice((prev) => ({ ...prev, affectation: e.target.value }))}
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="add-version">Version Logiciel</Label>
                  <Input
                    id="add-version"
                    placeholder="Ex: MR16.2..."
                    value={newDevice.version_logiciel}
                    onChange={(e) => setNewDevice((prev) => ({ ...prev, version_logiciel: e.target.value }))}
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="add-date-cle">Date dernier chiffrement</Label>
                  <Input
                    id="add-date-cle"
                    type="date"
                    value={newDevice.date_maj_cle}
                    onChange={(e) => setNewDevice((prev) => ({ ...prev, date_maj_cle: e.target.value }))}
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="add-obs">Observations</Label>
                <textarea
                  id="add-obs"
                  placeholder="Observations diverses, remarques sur l'état..."
                  value={newDevice.observation}
                  onChange={(e) => setNewDevice((prev) => ({ ...prev, observation: e.target.value }))}
                  className="w-full h-20 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 resize-none"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddDeviceModal(false)}
                  className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-bold transition-colors"
                >
                  Ajouter au Parc
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}

      {/* 4. ADD SITE TO CARTO MODAL */}
      {clickCoords && mapMode === "add_site" && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-sm border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <MapPin className="h-5 w-5 text-emerald-500 animate-bounce" />
                Déclarer un Nouveau Site
              </CardTitle>
              <button onClick={() => setClickCoords(null)} className="text-slate-500 hover:text-slate-300 focus:outline-none">
                ✕
              </button>
            </div>

            <form onSubmit={handleAddSite} className="space-y-4 font-mono text-xs">
              <div className="space-y-1.5">
                <Label htmlFor="site-nom-input">Nom du site géographique</Label>
                <Input
                  id="site-nom-input"
                  required
                  placeholder="Ex: Point Haut de Lure"
                  value={newSiteForm.nom}
                  onChange={(e) => setNewSiteForm((prev) => ({ ...prev, nom: e.target.value }))}
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="site-type-select">Type de site</Label>
                <select
                  id="site-type-select"
                  value={newSiteForm.type}
                  onChange={(e) => setNewSiteForm((prev) => ({ ...prev, type: e.target.value }))}
                  className="h-10 w-full bg-slate-950 border border-slate-800 rounded-lg px-3 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value="Point Haut">Point Haut</option>
                  <option value="CIS">CIS (Centre d'Incendie et de Secours)</option>
                  <option value="Centre Mixte">Centre Mixte</option>
                  <option value="Autre">Autre</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-500 bg-slate-950 p-2.5 rounded border border-slate-900">
                <div>Lat : {clickCoords.lat.toFixed(6)}</div>
                <div>Lng : {clickCoords.lng.toFixed(6)}</div>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setClickCoords(null)}
                  className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-bold transition-colors"
                >
                  Créer le Site
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}

      {/* 5. ADD LABEL TO CARTO MODAL */}
      {clickCoords && mapMode === "add_label" && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-sm border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <FileText className="h-5 w-5 text-emerald-500" />
                Poser une Étiquette
              </CardTitle>
              <button onClick={() => setClickCoords(null)} className="text-slate-500 hover:text-slate-300 focus:outline-none">
                ✕
              </button>
            </div>

            <form onSubmit={handleAddLabel} className="space-y-4 font-mono text-xs">
              <div className="space-y-1.5">
                <Label htmlFor="label-texte-input">Texte de l'étiquette libre</Label>
                <Input
                  id="label-texte-input"
                  required
                  placeholder="Ex: Liaison Secours Montagne"
                  value={newLabelForm.texte}
                  onChange={(e) => setNewLabelForm((prev) => ({ ...prev, texte: e.target.value }))}
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setClickCoords(null)}
                  className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-bold transition-colors"
                >
                  Poser l'Étiquette
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}

      {/* 6. ADD LIAISON MODAL */}
      {showLiaisonModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-sm border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <Activity className="h-5 w-5 text-emerald-500" />
                Tracer une Liaison Radio
              </CardTitle>
              <button
                onClick={() => setShowLiaisonModal(null)}
                className="text-slate-500 hover:text-slate-300 focus:outline-none"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddLiaison} className="space-y-4 font-mono text-xs">
              <div className="space-y-1 bg-slate-950 p-2.5 border border-slate-900 rounded text-slate-400">
                <div>De : <span className="text-slate-200 font-bold">{showLiaisonModal.siteA.nom}</span></div>
                <div>À : <span className="text-slate-200 font-bold">{showLiaisonModal.siteB.nom}</span></div>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="liaison-label-input">Label / Fréquence / Nom du lien</Label>
                <Input
                  id="liaison-label-input"
                  placeholder="Ex: Faisceau 5Ghz, Canaux UHF..."
                  value={newLiaisonForm.label}
                  onChange={(e) => setNewLiaisonForm((prev) => ({ ...prev, label: e.target.value }))}
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="liaison-color-input">Couleur du traceur graphique</Label>
                <div className="flex gap-2">
                  <input
                    id="liaison-color-input"
                    type="color"
                    value={newLiaisonForm.couleur}
                    onChange={(e) => setNewLiaisonForm((prev) => ({ ...prev, couleur: e.target.value }))}
                    className="h-10 w-12 bg-slate-950 border border-slate-800 rounded p-1"
                  />
                  <Input
                    type="text"
                    value={newLiaisonForm.couleur}
                    onChange={(e) => setNewLiaisonForm((prev) => ({ ...prev, couleur: e.target.value }))}
                    className="flex-1"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowLiaisonModal(null)}
                  className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-bold transition-colors"
                >
                  Créer la Liaison
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}

      {/* 7. ADD STOCK ITEM MODAL */}
      {showAddStockModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <Plus className="h-5 w-5 text-emerald-500" />
                Matériel Opérationnel de Réserve
              </CardTitle>
              <button
                onClick={() => setShowAddStockModal(false)}
                className="text-slate-500 hover:text-slate-300 focus:outline-none"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddStock} className="space-y-4 font-mono text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <Label htmlFor="stock-type-select">Catégorie de matériel</Label>
                  <select
                    id="stock-type-select"
                    value={newStockItem.type_materiel}
                    onChange={(e) => setNewStockItem((prev) => ({ ...prev, type_materiel: e.target.value }))}
                    className="h-10 w-full bg-slate-950 border border-slate-800 rounded-lg px-3 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600"
                  >
                    <option value="BIP">BIP (Radiomessagerie)</option>
                    <option value="Antares">Antares (Radio Numérique)</option>
                    <option value="Analogique">Analogique (Radio VHF/UHF)</option>
                    <option value="Accessoire">Accessoire Radio</option>
                    <option value="Autre">Autre Équipement</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="stock-etat-select">État initial</Label>
                  <select
                    id="stock-etat-select"
                    value={newStockItem.etat}
                    onChange={(e) => setNewStockItem((prev) => ({ ...prev, etat: e.target.value }))}
                    className="h-10 w-full bg-slate-950 border border-slate-800 rounded-lg px-3 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600"
                  >
                    <option value="Neuf">Neuf</option>
                    <option value="Excellent état">Excellent état</option>
                    <option value="Bon état">Bon état</option>
                    <option value="Usagé">Usagé</option>
                    <option value="En panne">En panne</option>
                  </select>
                </div>

                {/* Conditional Inputs based on stock type selection */}
                {["BIP", "Antares", "Analogique"].includes(newStockItem.type_materiel) ? (
                  <>
                    <div className="space-y-1.5">
                      <Label htmlFor="stock-modele">Modèle de Radio</Label>
                      <Input
                        id="stock-modele"
                        required
                        placeholder="Ex: TPG2200, GP340..."
                        value={newStockItem.modele}
                        onChange={(e) => setNewStockItem((prev) => ({ ...prev, modele: e.target.value }))}
                      />
                    </div>

                    <div className="space-y-1.5">
                      <Label htmlFor="stock-sn">Numéro de Série (S/N)</Label>
                      <Input
                        id="stock-sn"
                        required
                        placeholder="N° série unique..."
                        value={newStockItem.num_serie}
                        onChange={(e) => setNewStockItem((prev) => ({ ...prev, num_serie: e.target.value }))}
                      />
                    </div>

                    <div className="space-y-1.5">
                      <Label htmlFor="stock-cis">CIS d'origine / stockage</Label>
                      <Input
                        id="stock-cis"
                        required
                        placeholder="Ex: CIS Digne..."
                        value={newStockItem.cis}
                        onChange={(e) => setNewStockItem((prev) => ({ ...prev, cis: e.target.value }))}
                      />
                    </div>

                    {newStockItem.type_materiel === "BIP" && (
                      <div className="space-y-1.5">
                        <Label htmlFor="stock-pocsag">Code POCSAG</Label>
                        <Input
                          id="stock-pocsag"
                          required
                          placeholder="Ex: 0123456..."
                          value={newStockItem.pocsag}
                          onChange={(e) => setNewStockItem((prev) => ({ ...prev, pocsag: e.target.value }))}
                        />
                      </div>
                    )}

                    {newStockItem.type_materiel === "Antares" && (
                      <div className="space-y-1.5">
                        <Label htmlFor="stock-rfgi">Code RFGI</Label>
                        <Input
                          id="stock-rfgi"
                          required
                          placeholder="Ex: 208..."
                          value={newStockItem.rfgi}
                          onChange={(e) => setNewStockItem((prev) => ({ ...prev, rfgi: e.target.value }))}
                        />
                      </div>
                    )}

                    {newStockItem.type_materiel === "Analogique" && (
                      <div className="space-y-1.5">
                        <Label htmlFor="stock-identifiant">Identifiant Réseau</Label>
                        <Input
                          id="stock-identifiant"
                          required
                          placeholder="Ex: CC-04..."
                          value={newStockItem.identifiant}
                          onChange={(e) => setNewStockItem((prev) => ({ ...prev, identifiant: e.target.value }))}
                        />
                      </div>
                    )}
                  </>
                ) : (
                  <div className="space-y-1.5 col-span-2">
                    <Label htmlFor="stock-nom-libre">Désignation libre du matériel</Label>
                    <Input
                      id="stock-nom-libre"
                      required
                      placeholder="Ex: Chargeur Rapide Antares, Batterie..."
                      value={newStockItem.nom}
                      onChange={(e) => setNewStockItem((prev) => ({ ...prev, nom: e.target.value }))}
                    />
                  </div>
                )}
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="stock-desc">Description complémentaire / Observations</Label>
                <textarea
                  id="stock-desc"
                  placeholder="Informations supplémentaires..."
                  value={newStockItem.description}
                  onChange={(e) => setNewStockItem((prev) => ({ ...prev, description: e.target.value }))}
                  className="w-full h-20 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 resize-none"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddStockModal(false)}
                  className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-bold transition-colors"
                >
                  Enregistrer
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}

      {/* 8. CREATE LOAN MODAL */}
      {showLoanModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-sm border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <Package className="h-5 w-5 text-blue-500" />
                Enregistrer un Emprunt
              </CardTitle>
              <button
                onClick={() => setShowLoanModal(null)}
                className="text-slate-500 hover:text-slate-300 focus:outline-none"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateLoan} className="space-y-4 font-mono text-xs">
              <div className="bg-slate-950 p-2.5 border border-slate-900 rounded font-mono text-slate-300 mb-2 text-center font-bold">
                Matériel : {showLoanModal.nom}
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="loan-emprunteur">Emprunteur (Nom / Service / CIS)</Label>
                <Input
                  id="loan-emprunteur"
                  required
                  placeholder="Ex: Sgt. Dupont (CIS Forcalquier)"
                  value={loanForm.emprunteur}
                  onChange={(e) => setLoanForm((prev) => ({ ...prev, emprunteur: e.target.value }))}
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <Label htmlFor="loan-debut">Date de début</Label>
                  <Input
                    id="loan-debut"
                    type="date"
                    required
                    value={loanForm.date_debut}
                    onChange={(e) => setLoanForm((prev) => ({ ...prev, date_debut: e.target.value }))}
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="loan-fin">Date de retour prévue</Label>
                  <Input
                    id="loan-fin"
                    type="date"
                    required
                    value={loanForm.date_fin}
                    onChange={(e) => setLoanForm((prev) => ({ ...prev, date_fin: e.target.value }))}
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowLoanModal(null)}
                  className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs rounded font-bold transition-colors"
                >
                  Confirmer le Prêt
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}

      {/* 9. RETURN LOAN MODAL */}
      {showReturnModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-sm border border-slate-800 bg-slate-900 p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <CardTitle className="text-base text-white font-mono flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                Enregistrer le Retour
              </CardTitle>
              <button
                onClick={() => setShowReturnModal(null)}
                className="text-slate-500 hover:text-slate-300 focus:outline-none"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleReturnLoan} className="space-y-4 font-mono text-xs">
              <div className="bg-slate-950 p-2.5 border border-slate-900 rounded font-mono text-slate-300 mb-2 text-center font-bold">
                Retour : {showReturnModal.nom}
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="return-status-select">Nouveau statut d'état du matériel</Label>
                <select
                  id="return-status-select"
                  value={returnForm.nouveau_statut_etat}
                  onChange={(e) => setReturnForm((prev) => ({ ...prev, nouveau_statut_etat: e.target.value }))}
                  className="h-10 w-full bg-slate-950 border border-slate-800 rounded-lg px-3 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value="Neuf">Neuf</option>
                  <option value="Excellent état">Excellent état</option>
                  <option value="Bon état">Bon état</option>
                  <option value="Usagé">Usagé</option>
                  <option value="En panne">En panne</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="return-notes">Modifications ou remarques d'état</Label>
                <textarea
                  id="return-notes"
                  placeholder="Saisir d'éventuels dégâts constatés ou remarques..."
                  value={returnForm.changement_etat}
                  onChange={(e) => setReturnForm((prev) => ({ ...prev, changement_etat: e.target.value }))}
                  className="w-full h-20 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 resize-none"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowReturnModal(null)}
                  className="px-4 py-2 bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded hover:bg-slate-800 transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded font-bold transition-colors"
                >
                  Valider le Retour
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}

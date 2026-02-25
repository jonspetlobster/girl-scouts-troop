// Girl Scouts Troop Materials - Client-Side Search

class TroopSearch {
  constructor() {
    this.searchInput = document.getElementById('search-input');
    this.searchableCards = document.querySelectorAll('.card[data-searchable]');
    this.noResults = document.getElementById('no-results');
    
    if (this.searchInput) {
      this.init();
    }
  }

  init() {
    // Add event listener for search input
    this.searchInput.addEventListener('input', (e) => {
      this.performSearch(e.target.value);
    });

    // Add event listener for clear button if exists
    const clearBtn = document.getElementById('clear-search');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        this.clearSearch();
      });
    }
  }

  performSearch(query) {
    const searchTerm = query.toLowerCase().trim();
    
    if (searchTerm === '') {
      this.showAllCards();
      this.hideNoResults();
      return;
    }

    let visibleCount = 0;

    this.searchableCards.forEach(card => {
      const searchableText = card.getAttribute('data-searchable').toLowerCase();
      const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
      const description = card.querySelector('.card-description')?.textContent.toLowerCase() || '';
      const badges = Array.from(card.querySelectorAll('.card-badge'))
        .map(b => b.textContent.toLowerCase())
        .join(' ');
      
      // Combine all searchable content
      const allContent = `${searchableText} ${title} ${description} ${badges}`;
      
      // Check if search term matches
      if (allContent.includes(searchTerm)) {
        this.showCard(card);
        this.highlightMatches(card, searchTerm);
        visibleCount++;
      } else {
        this.hideCard(card);
      }
    });

    // Show/hide no results message
    if (visibleCount === 0) {
      this.showNoResults(searchTerm);
    } else {
      this.hideNoResults();
    }
  }

  showCard(card) {
    card.style.display = '';
    card.classList.remove('hidden');
  }

  hideCard(card) {
    card.style.display = 'none';
    card.classList.add('hidden');
  }

  showAllCards() {
    this.searchableCards.forEach(card => {
      this.showCard(card);
      this.removeHighlights(card);
    });
  }

  highlightMatches(card, searchTerm) {
    // Optional: Add a subtle highlight to matched cards
    card.style.borderColor = '#00ae58';
    card.style.borderWidth = '2px';
  }

  removeHighlights(card) {
    card.style.borderColor = '';
    card.style.borderWidth = '';
  }

  showNoResults(term) {
    if (this.noResults) {
      this.noResults.classList.remove('hidden');
      const termSpan = this.noResults.querySelector('.search-term');
      if (termSpan) {
        termSpan.textContent = term;
      }
    }
  }

  hideNoResults() {
    if (this.noResults) {
      this.noResults.classList.add('hidden');
    }
  }

  clearSearch() {
    this.searchInput.value = '';
    this.showAllCards();
    this.hideNoResults();
    this.searchInput.focus();
  }
}

// Initialize search when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new TroopSearch();
  
  // Set active nav link
  setActiveNavLink();
});

// Set active navigation link based on current page
function setActiveNavLink() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.navbar-nav a');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

// Utility: Format dates nicely
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

// Utility: Calculate days since update
function daysSince(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diff = Math.floor((now - date) / (1000 * 60 * 60 * 24));
  
  if (diff === 0) return 'Today';
  if (diff === 1) return 'Yesterday';
  if (diff < 7) return `${diff} days ago`;
  if (diff < 30) return `${Math.floor(diff / 7)} weeks ago`;
  if (diff < 365) return `${Math.floor(diff / 30)} months ago`;
  return `${Math.floor(diff / 365)} years ago`;
}

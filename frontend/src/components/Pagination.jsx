import { FiChevronLeft, FiChevronRight } from "react-icons/fi";

/**
 * Pagination component for search results
 * @param {Object} props
 * @param {number} props.currentPage - Current page (1-indexed)
 * @param {number} props.totalResults - Total number of results
 * @param {number} props.pageSize - Results per page
 * @param {Function} props.onPageChange - Callback when page changes
 */
export default function Pagination({
  currentPage = 1,
  totalResults = 0,
  pageSize = 20,
  onPageChange,
}) {
  const totalPages = Math.ceil(totalResults / pageSize);

  if (totalPages <= 1) {
    return null;
  }

  const startResult = (currentPage - 1) * pageSize + 1;
  const endResult = Math.min(currentPage * pageSize, totalResults);

  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  const handlePageClick = (page) => {
    if (page !== currentPage) {
      onPageChange(page);
    }
  };

  // Generate page numbers to display
  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;

    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Always show first page
      pages.push(1);

      if (currentPage > 3) {
        pages.push("...");
      }

      // Show pages around current page
      const start = Math.max(2, currentPage - 1);
      const end = Math.min(totalPages - 1, currentPage + 1);

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      if (currentPage < totalPages - 2) {
        pages.push("...");
      }

      // Always show last page
      pages.push(totalPages);
    }

    return pages;
  };

  return (
    <div className="flex items-center justify-between py-6 border-t border-gray-200 dark:border-gray-700">
      {/* Results info */}
      <div className="text-sm text-gray-600 dark:text-gray-400">
        Showing <span className="font-medium text-gray-900 dark:text-gray-100">{startResult}</span> to{" "}
        <span className="font-medium text-gray-900 dark:text-gray-100">{endResult}</span> of{" "}
        <span className="font-medium text-gray-900 dark:text-gray-100">{totalResults}</span> results
      </div>

      {/* Page controls */}
      <div className="flex items-center gap-2">
        {/* Previous button */}
        <button
          onClick={handlePrevious}
          disabled={currentPage === 1}
          className="
            p-2 rounded-lg border
            bg-white dark:bg-gray-800
            border-gray-200 dark:border-gray-700
            text-gray-700 dark:text-gray-300
            disabled:opacity-50 disabled:cursor-not-allowed
            hover:bg-gray-50 dark:hover:bg-gray-700
            transition-all duration-200
          "
          aria-label="Previous page"
        >
          <FiChevronLeft className="h-5 w-5" />
        </button>

        {/* Page numbers */}
        <div className="flex items-center gap-1">
          {getPageNumbers().map((page, idx) => {
            if (page === "...") {
              return (
                <span
                  key={`ellipsis-${idx}`}
                  className="px-3 py-2 text-gray-400 dark:text-gray-600"
                >
                  ...
                </span>
              );
            }

            return (
              <button
                key={page}
                onClick={() => handlePageClick(page)}
                className={`
                  min-w-[2.5rem] px-3 py-2 rounded-lg border text-sm font-medium
                  transition-all duration-200
                  ${
                    page === currentPage
                      ? "bg-brand-blue text-white border-brand-blue"
                      : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                  }
                `}
              >
                {page}
              </button>
            );
          })}
        </div>

        {/* Next button */}
        <button
          onClick={handleNext}
          disabled={currentPage === totalPages}
          className="
            p-2 rounded-lg border
            bg-white dark:bg-gray-800
            border-gray-200 dark:border-gray-700
            text-gray-700 dark:text-gray-300
            disabled:opacity-50 disabled:cursor-not-allowed
            hover:bg-gray-50 dark:hover:bg-gray-700
            transition-all duration-200
          "
          aria-label="Next page"
        >
          <FiChevronRight className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}
